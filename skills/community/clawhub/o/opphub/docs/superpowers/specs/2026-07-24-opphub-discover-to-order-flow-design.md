# OppHub 发现→撮合→消息→订单 流程重构设计

**Date**: 2026-07-24
**Status**: draft
**Author**: 后端程序猿 (OpenClaw bot)
**Scope**: opphub-web (Next.js) + opphub-ws (推送服务) + Prisma schema
**关联 spec**:
- `docs/superpowers/specs/2026-07-23-opphub-product-design.md` (产品总架构, 主参考)
- `docs/v3.1-architecture.md` (推送链架构)
- `docs/superpowers/plans/2026-07-23-phase5-v1-conflicts-radar.md` (当前 /discover V1 实现依据)

---

## 0. 背景与问题

### 0.1 一句话

`/discover` 的"进入撮合" CTA 触发了 `POST /api/matchings`,但这条链路**绕过了 opphub-ws 推送管道**,并且**没有后续的咨询/出价/订单状态机**。从发现 → 撮合 → 消息 → 订单这条主链路当前只跑通了第 1 步。

### 0.2 现状(对照 `2026-07-23-opphub-product-design.md` §2.3 钉死的 8 步状态机)

| spec 状态 | spec 章节 | 现状 | 文件:行 |
|---|---|---|---|
| `OpcMatching.status = pending` | §2.3 | ✅ 已实现 | `opphub-web/prisma/schema.prisma:266` |
| `OpcMatching.status = active` (接受撮合) | - | ✅ 已实现 (语义=已开聊天, 对应 spec 的 inquiry) | `app/api/matchings/[id]/route.ts:83` |
| `OpcMatching.status = declined` | §2.3 | ✅ 已实现 | schema:274 + route.ts:84 |
| `OpcMatching.status = cancelled` | - | ✅ 已实现 (cancelled 而不是 spec 的 declined/closed) | route.ts:85, messages/route.ts:94 引用 |
| `OpcMatching.status = inquiry` (任一方发起咨询) | §2.3 | ⚠️ 现有 `active` 语义等同 inquiry, 但命名跟 spec 不一致, **需 enum 迁移** | - |
| `OpcMatching.status = bid_pending` (我方出价) | §2.3 | ❌ 缺 (无出价 endpoint) | - |
| `OpcMatching.status = bid_accepted` (对方接受) | §2.3 | ❌ 缺 | - |
| `OpcMatching.status = expired/archived` | §2.3 | ❌ 缺 cron | - |
| `Order` 表 (status: pending→paid→in_progress→delivered→accepted→completed/disputed/refunded) | §2.3 | ⚠️ 有 Order 表 (schema:391) 但跟 OpcMatching 无外键关联, 没接入状态机。老 Demand 模型专用 | schema:391 |
| `Payment` (escrow/release/refund/commission) | §2.3 | ❌ | schema 缺 |
| 撮合内聊天 endpoint (`/api/matchings/[id]/messages`) | - | ✅ 已实现 | `app/api/matchings/[id]/messages/route.ts` |
| 已读 endpoint (`/api/matchings/[id]/messages/read`) | - | ✅ 已实现 | `app/api/matchings/[id]/messages/read/route.ts` |
| 接受/拒绝/取消 endpoint (`PATCH /api/matchings/[id]`) | - | ✅ 已实现 (`accept`→`active` / `decline`→`declined` / `cancel`→`cancelled`) | `app/api/matchings/[id]/route.ts` |
| `OpcTrustScore` 表 | §4.3 | ✅ 已实现 (default 60), 但没接入匹配评分 | `schema.prisma:238` |

### 0.3 推送管道绕过(spec §5.3 + §8.3 钉死)

- **钉死**: opphub-web 不直连 FCM/微信/短信, 必须走 opphub-ws `POST /push`(`opphub-ws/ws-server.js:768`)
- **现状**: `opphub-web/app/api/matchings/route.ts:178-195` 直接 `prisma.pendingMessage.create({ type: "matching_chat", opcId: otherEntry.opcId, payload: {...} })`
- **后果**:
  - `ws-server.js:128` 的 `deliveredMessageIds` 去重表对这条消息失效
  - `ws-server.js:744-760` 的 ack 重试 (1st/5min/1h) 失效
  - 死信机制不存在
  - PushLog 表没建 (spec §5.3)
  - 双方推送 (spec §4.1) 缺, 当前只给对方推

### 0.4 评分公式不匹配 (spec §4.3 vs 现状)

**spec §4.3**:
```
match_score = 0.40·semantic + 0.20·price_match + 0.15·geo_match + 0.15·trust_score + 0.10·recency
```

**现状** `opphub-web/app/api/matchings/route.ts:32-45`:
```
0.4 基线 + 0.40·维度匹配 + 0.10·industry + 0.05·city
```

| 维度 | spec | 现状 | 备注 |
|---|---|---|---|
| semantic (embedding cosine) | 0.40 | ❌ 缺 | `opc_knowledge_chunk` 表存在 (schema:219), embedding `vector(768)` (BGE 本地 ONNX), 但没接入 cosine 计算 |
| price_match (区间重叠) | 0.20 | ❌ 缺 | `parsedFields` 没结构化价格字段 |
| geo_match (同城) | 0.15 | ⚠️ 0.05 | 权重低于 spec |
| trust_score | 0.15 | ⚠️ **可立即接入** | `OpcTrustScore` 表 (schema:238) 已存在, 默认 60, 但没参与匹配评分 |
| recency (7d 加权) | 0.10 | ❌ 缺 | - |

### 0.5 其他规范缺口

| 项 | spec | 现状 |
|---|---|---|
| 频控 | §4.6 同对 1d 最多一次 / OPC 一周 30 / declined 14d 不再推 | ❌ 无任何限流 (route.ts 107-153 去重逻辑混乱) |
| 匿名 | §4.7 撮合卡片只显示 维度+城市+评分 | ❌ `discover/page.tsx:138-141` 直接抓 `companyName` |
| 5 状态规范 | §6 loading/empty/error/unauth/未实名 | ❌ discover 大半是 inline style + ad-hoc |
| 导航 | §1.1 `/matches` 替代 `/match` | ❌ 两个都存在, 无 redirect (`app/match/page.tsx` + `app/matches/page.tsx`) |
| 推送通道优先级 | §5.4 fcm > email > wechat > sms | ⚠️ 仅 IM (pending_message → ws-server → plugin), 没多通道 fallback |

### 0.6 老 Demand 模型并存 (开放问题)

`prisma/schema.prisma` 里同时存在两套撮合模型:

- **新 OppHub 模型**: `OpcMatching` + `OpcMatchingMessage` + `OpcKnowledgeEntry` (ability/downstream)
- **老 R2 Demand 模型**: `Demand` + `MatchingRecord` + `Bid` + `Order` (Demand 侧需求 → 应单 → 订单)

老的 `Bid` 表 (schema:479) 是 OPC 应 Demand 的单;新 OpcMatching 是 AI 撮合的对,两者没有外键桥接。本次 spec **不处理老模型去留**, 留作 §11 开放问题。

---

## 1. 目标与非目标

### 1.1 目标

1. **接通推送管道**: `POST /api/matchings` 不再直接写 `pending_message`,改调 `opphub-ws POST /push`
2. **完整状态机**: `OpcMatching.status` 扩展到 spec §2.3 的 8 个状态
3. **评分公式升级**: 引入 semantic (BGE 768 cosine) + recency, 补齐 geo 权重
4. **运营基础**: PushLog 表 + 频控 + 死信入口
5. **导航收尾**: `/match` 301 → `/matches`

### 1.2 非目标 (YAGNI)

- ❌ Payment 表 + 钱包流程 (spec §2.3 payments, 留作阶段 7 钱包)
- ❌ `Demand` / `MatchingRecord` / `Bid` 老模型的去留 / 桥接
- ❌ 多通道 fallback (email / 微信 / 短信), 当前 IM 走通即可
- ❌ trust_score 信用分**新机制** (历史订单完成率 / 评分建模) — spec §4.3 钉死
- ✅ trust_score 接入匹配评分 — `OpcTrustScore` 表 (schema:238) 已实现, 批 2 直接用, 不需要新建机制
- ❌ price_match 区间匹配 (parsedFields 没结构化价格, 需先扩字段)
- ❌ 争议 (dispute) 流程 UI
- ❌ 后台手动撮合池 (`/admin/match-pool`, spec §4.5)

---

## 2. 改进方案分批

| 批 | 内容 | 工作量 | 依赖 |
|---|---|---|---|
| 批 1 | 推送管道接通 (根问题) | 1.5d | 无 |
| 批 2 | 评分公式升级 + 频控 + 匿名 | 2d | 批 1 |
| 批 3 | 状态机补全 (inquiry / bid / accept / decline) | 2d | 批 1 |
| 批 4 | 运营基础 (PushLog + 死信 + 导航收尾) | 1.5d | 批 1 |
| **合计** | | **7.5d** | |

每批独立可发布;舟哥可决定开哪批。本次 spec 设计覆盖全部 4 批, plan 实施可分批执行。

---

## 3. 批 1: 推送管道接通 (根问题)

### 3.1 现状 vs 改造

**现状** (`opphub-web/app/api/matchings/route.ts:178-195`):
```ts
await prisma.pendingMessage.create({
  data: {
    opcId: otherEntry.opcId,
    type: "matching_chat",                  // ⚠️ 不是 spec 定义的 type
    score: 80,
    payload: { matchingId, fromOpcId, fromName, title, desc, text, otherDimension, otherEntryId },
    expiredAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
  },
});
```

**改造后**:
```ts
// 1. server 端发 system 事件给双方 (调 opphub-ws POST /push)
// 2. 不再 prisma.pendingMessage.create (由 opphub-ws 接管)
await pushViaWs({
  userId: otherEntry.opcId,
  message: {
    type: "match",
    matchingId: matching.id,
    otherOpcId: fromOpcId,
    otherEntryId: otherEntryId,
    otherDimension: dimensionLabel,
    matchScore: finalScore,
    text: trimmedMessage,
    title: `${fromName} 想跟你聊聊「${dimensionLabel}」`,
    // ... 透传字段
  },
});
```

### 3.2 opphub-ws 鉴权解决

`ws-server.js:822` 钉死的鉴权: `caller.isAdmin || caller.opcId === userId`。

server 内部推送对方时, caller 是 fromOpcId 不是对方, 会触发 403 forbidden。

**方案 A (推荐, 改 server 端鉴权规则)**:

`opphub-ws/ws-server.js:822` 增加 system 事件白名单:
```js
const SYSTEM_TRIGGERS = ['match.created', 'match.inquiry', 'match.bid_accepted', 'order.created'];
if (!caller.isAdmin && caller.opcId !== userId) {
  // system trigger 由 matching/order 系统代发, 允许
  if (!SYSTEM_TRIGGERS.includes(message.event) || !caller.isAdmin) {
    return 403 forbidden;
  }
}
```

理由: system 事件 (撮合通知 / 订单通知) 的发起方是 server 内部业务流, 不是用户自发;鉴权层只要"是合法 OPC 触发的业务事件"即可。

**方案 B (用 admin JWT 调 /push)**: server 维护一个 `OPPHUB_SERVICE_JWT` (isAdmin=true), 业务流都用这个调 /push。
- 缺点: 跟当前 ws-server 鉴权语义不一致, 需要在 server 端额外管理 service token

**采用 A**。风险小,改动局部。

### 3.3 双方推送 (spec §4.1)

新增逻辑: 不仅给对方推, 也给自己推一份"撮合已发起"。

```ts
// 给对方
await pushViaWs({ userId: otherEntry.opcId, message: { type: 'match', event: 'match.created', ... } });
// 给自己 (撮合记录 mirror)
await pushViaWs({ userId: fromOpcId, message: { type: 'match', event: 'match.created', role: 'from', ... } });
```

前端 `/matches` 列表用 `role=from|to|both` 查询 (route.ts:215 已支持)。

### 3.4 payload schema (收紧)

替代 route.ts:183 那一坨字段:

```ts
type MatchPushPayload = {
  type: 'match';
  event: 'match.created' | 'match.inquiry' | 'match.bid' | 'match.bid_accepted' | 'match.declined';
  matchingId: string;
  otherOpcId: string;       // 对方
  otherDisplayName: string; // 对方 displayName 或 companyName (供 frontend 渲染)
  otherEntryId: string;
  otherDimension: string;
  matchScore: number;       // 0-1
  text?: string;            // 撮合留言 (匹配发起时的 message 字段)
  createdAt: string;        // ISO
};
```

### 3.5 改动文件

| 文件 | 改动 |
|---|---|
| `opphub-web/app/api/matchings/route.ts` | 删除 178-195 直接 `pendingMessage.create`, 改为 `pushViaWs()` 调 opphub-ws |
| `opphub-web/lib/push.ts` (新) | `pushViaWs(userId, message)` 封装 HTTP POST `opphub-ws:PORT/push` |
| `opphub-ws/ws-server.js:822` | 增加 `SYSTEM_TRIGGERS` 白名单 |

---

**批 1 实施 (2026-07-24, commit 链):**

| commit | repo | 改动 |
|---|---|---|
| `28e2e35` | opphub-web submodule | `lib/push.ts` 新建 + 4 个单元测试 (`pushViaWs()` + service JWT 鉴权) |
| `5920169` | opphub-web submodule | `app/api/matchings/route.ts` 改造, 双方推送 (pushToOther + pushToSelf) + 失败退路写 pending_message |
| `9758ec1` | opphub-web submodule | fallback `type: 'matching_chat'` → `'credit'` (schema 合法值), 首次创建 fallback 用 `pushArgs` schema |
| `2f32843` | opphub-web submodule | `pushViaWs()` service JWT 加 `opcId: 'service:push'` (ws-server.js:810 强制要求) |
| `1bf6842` | opphub-ws 独立 repo | `ws-server.js` 加 `SYSTEM_TRIGGERS` 白名单 (10 个 event), `__tests__/system-triggers-whitelist.test.js` (4/4 通过) |
| `f3b7427` `5b51988` `7daf717` | main repo | submodule bump commits |

**端到端验证 (Task 4)**: 起 ws-server (WS_PORT=13003, MOCK_DB=1), 模拟 pushViaWs 完整调用 → admin caller match.created ✅, biz caller (非 admin) match.created 通过白名单 ✅, biz caller dm 仍 403 ✅, biz caller 乱写 event 仍 403 ✅.

**遗留 (留作后续批次)**:
- 双方推送当前是 best-effort 给自己 (失败只 warn 不退路), 严格应退路写 pending_message — 留作批 2 顺手补
- fallback payload schema 第一处统一用 pushArgs, 第二处 (retry) 仍用原 schema (title/desc/text) — 后续批 3 可统一

## 4. 批 2: 评分公式升级 + 频控 + 匿名

### 4.1 新评分公式

```ts
async function calcMatchScore(fromEntry, toEntry, fromOpc, toOpc): Promise<number> {
  // semantic: 取 fromEntry 和 toEntry 最新 chunk 的 embedding 算 cosine
  const fromEmb = await getLatestEmbedding(fromEntry.id);
  const toEmb = await getLatestEmbedding(toEntry.id);
  const semantic = fromEmb && toEmb ? cosine(fromEmb, toEmb) : 0;
  
  // geo: 同城 +1
  const geo = fromEntry.parsedFields?.city && toEntry.parsedFields?.city 
              && fromEntry.parsedFields.city === toEntry.parsedFields.city ? 1 : 0;
  
  // dim: 维度匹配
  const dim = fromEntry.entryDimension === toEntry.entryDimension ? 1 
              : (fromEntry.entryDimension?.includes(toEntry.entryDimension) ? 0.5 : 0);
  
  // industry: 同业 +1
  const industry = fromEntry.parsedFields?.industry?.name === toEntry.parsedFields?.industry?.name ? 1 : 0;
  
  // recency: 7 天内录入加权
  const daysSince = Math.min(7, (Date.now() - newEntry(toEntry).createdAt) / 86400000);
  const recency = 1 - daysSince / 7;
  
  // 总分 (无 price / trust, 占位 0)
  const total = 0.40 * semantic + 0.15 * geo + 0.20 * dim + 0.15 * industry + 0.10 * recency;
  return Math.round(Math.min(total, 0.99) * 100) / 100;
}
```

### 4.2 embedding 来源

`opc_knowledge_chunk.embedding` (`schema.prisma:...`, 需 grep 确认) 是 BGE 768 维向量。
- 取每个 entry 最新一条 chunk (按 createdAt desc limit 1)
- pgvector `<=>` cosine operator 算距离, 1 - distance = similarity

```sql
SELECT 1 - (c1.embedding <=> c2.embedding) AS cosine
FROM opc_knowledge_chunk c1, opc_knowledge_chunk c2
WHERE c1.entry_id = $1 AND c2.entry_id = $2
ORDER BY c1.created_at DESC, c2.created_at DESC
LIMIT 1;
```

### 4.3 频控 (spec §4.6)

在 `POST /api/matchings` 入口加:

```ts
// 1. 同对 24h 限一次
const recent = await prisma.opcMatching.findFirst({
  where: {
    fromOpcId,
    toEntryId: otherEntryId,
    createdAt: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) },
    status: { in: ['pending', 'inquiry', 'bid_pending', 'bid_accepted'] },
  },
});
if (recent) {
  return NextResponse.json({
    ok: false, error: 'duplicate',
    message: '24h 内已撮合过这对, 等待对方回应',
    matchingId: recent.id,
  }, { status: 409 });
}

// 2. OPC 一周 30 上限
const weekCount = await prisma.opcMatching.count({
  where: { fromOpcId, createdAt: { gte: new Date(Date.now() - 7 * 86400000) } },
});
if (weekCount >= 30) {
  return NextResponse.json({
    ok: false, error: 'rate_limited',
    message: '本周撮合已达 30 条上限',
  }, { status: 429 });
}

// 3. declined 14d 不再推
const recentlyDeclined = await prisma.opcMatching.findFirst({
  where: {
    fromOpcId, toEntryId: otherEntryId, status: 'declined',
    createdAt: { gte: new Date(Date.now() - 14 * 86400000) },
  },
});
if (recentlyDeclined) {
  return NextResponse.json({
    ok: false, error: 'declined_cooldown',
    message: '对方已拒绝, 14 天内不再推送',
  }, { status: 409 });
}
```

### 4.4 匿名 (spec §4.7)

`/discover` 页面改显示:

| 字段 | 当前 | spec |
|---|---|---|
| 对方名称 | `companyName` (直接显示) | ❌ 改为 `其他提供方 · #A001` 匿名代号 (撮合前) |
| 维度 | `entryDimension` | ✅ 保留 |
| 城市 | `parsedFields.city` | ✅ 保留 |
| 评分 | `matchScore` | ✅ 保留 |
| 公司名 | ❌ | 显示在 `发起咨询后` 解锁 (本期未做 inquiry, 暂保留显示) |

**本期简化**: discover 页保持显示 companyName (用户当前可见度诉求高), 但在 `/matches/[id]` 撮合详情页加"匿名模式"开关, 默认匿名, 点"发起咨询"后解锁。discover 页本身的"匿名化"留作后续 (涉及 UI 改版)。

---

## 5. 批 3: 状态机补全 (inquiry / bid / accept / decline)

### 5.1 状态机 (spec §2.3 钉死, 现状部分实现)

**现状已实现**: `pending` / `active` / `declined` / `cancelled` (4 个)

**扩展到 spec §2.3 钉死的 8 个状态**, Prisma enum:

```prisma
enum MatchingStatus {
  pending          // AI 发现, 双方没人看 ✅ 已有
  inquiry          // 任一方发起咨询 (打开了聊天) ⚠️ active → inquiry (重命名, 语义同)
  bid_pending      // 已出价, 等回应
  bid_countered    // 还价
  bid_accepted     // 出价被接受 = 形成订单
  declined         // 拒绝/忽略 ✅ 已有
  cancelled        // 发起方取消 ✅ 已有 (保留, 非 spec 但合理)
  expired          // 30d 无响应
  archived         // 30d 后归档
}
```

迁移 SQL:
```sql
-- active 重命名为 inquiry (语义不变)
UPDATE opc_matching SET status = 'inquiry' WHERE status = 'active';
-- 现有 PATCH /api/matchings/[id] accept 把 status 写为 'active' 改为 'inquiry'
```

**复用现有 PATCH 端点**: `app/api/matchings/[id]/route.ts:82-86` 现有 `statusMap` 已包含 `accept→active / decline→declined / cancel→cancelled`, 改造为 `accept→inquiry`, 然后在 `accept` 分支后续增加 `bid` / `accept_bid` / `counter_bid` 等 action。

### 5.2 新表

**OpcMatchingBid** (出价) — `OpcMatching` 的子记录:
```prisma
model OpcMatchingBid {
  id          String   @id @default(cuid())
  matchingId  String   @map("matching_id")
  fromOpcId   String   @map("from_opc_id")
  amount      Decimal  @db.Decimal(10, 2)
  termDays    Int      @map("term_days")
  msg         String?  @db.Text
  status      String   @default("pending") // pending / accepted / rejected / countered
  parentBidId String?  @map("parent_bid_id") // 还价时指向上一轮
  createdAt   DateTime @default(now()) @map("created_at")
  decidedAt   DateTime? @map("decided_at")

  matching OpcMatching @relation(fields: [matchingId], references: [id], onDelete: Cascade)

  @@index([matchingId, createdAt])
  @@map("opc_matching_bid")
}
```

### 5.3 新 API (复用现有 + 增量)

**复用现有** (route.ts 已有):
- `PATCH /api/matchings/[id]` body=`{action: 'accept'|'decline'|'cancel'}` — 改为 `accept → inquiry / decline → declined / cancel → cancelled`
- `GET/POST /api/matchings/[id]/messages` — 撮合内聊天, ✅ 已实装
- `POST /api/matchings/[id]/messages/read` — 标记已读, ✅ 已实装

**新增** (批 3 实装):
| Method | Path | Body | Effect |
|---|---|---|---|
| `POST` | `/api/matchings/[id]/bid` | `{ amount, termDays, msg? }` | matching.status: inquiry → bid_pending; 建 OpcMatchingBid; 给对方 push `event: 'match.bid'` |
| `POST` | `/api/matchings/[id]/accept-bid` | `{ bidId }` | matching.status: bid_pending → bid_accepted; 建 OpcMatchingOrder; 给双方 push `event: 'match.bid_accepted'` |
| `POST` | `/api/matchings/[id]/counter` | `{ amount, termDays, msg? }` | matching.status: bid_pending → bid_countered; 建新 OpcMatchingBid (parentBidId 指上一轮) |
| `GET` | `/api/matchings/[id]/bids` | — | 列所有 OpcMatchingBid (按 createdAt asc) |

### 5.4 Order 创建

`accept` 成功时:

```ts
const order = await prisma.order.create({
  data: {
    orderNo: `M${Date.now()}${randomBytes(2).toString('hex')}`,
    opcId: fromOpcId,         // 需求方 (出价被接受方 / 付款方)
    supplierOpcId: toOpcId,   // 供应方
    demandId: null,            // ⚠️ 老 Demand 模型字段, 暂留 null
    amount: bid.amount,
    payChannel: 'wechat',     // 占位
    recvChannel: 'wechat',
    platformFee: bid.amount * 0.05,  // spec §2.3 钉死 5%
    status: 'pending',
  },
});
```

注: `Order.demandId` 当前 schema 是必填 (NOT NULL)。要么 (a) 改为 nullable, 要么 (b) 不建 Order 桥接老 Demand, 改建新表 `opc_matching_order`。**采用 (b)**: 建新表 `OpcMatchingOrder`, 老 Demand 模型不动 (避免破坏老数据)。

```prisma
model OpcMatchingOrder {
  id          String   @id @default(cuid())
  matchingId  String   @unique @map("matching_id")  // 1 matching → 1 order
  fromOpcId   String   @map("from_opc_id")          // 需求方
  toOpcId     String   @map("to_opc_id")            // 供应方
  bidId       String   @map("bid_id")
  amount      Decimal  @db.Decimal(10, 2)
  platformFee Decimal  @map("platform_fee") @db.Decimal(10, 2)
  status      String   @default("pending")  // pending / paid / in_progress / delivered / accepted / completed / disputed / cancelled / refunded
  createdAt   DateTime @default(now()) @map("created_at")
  paidAt      DateTime? @map("paid_at")
  deliveredAt DateTime? @map("delivered_at")
  acceptedAt  DateTime? @map("accepted_at")

  matching OpcMatching @relation(fields: [matchingId], references: [id])
  bid OpcMatchingBid @relation(fields: [bidId], references: [id])

  @@index([fromOpcId, status])
  @@index([toOpcId, status])
  @@map("opc_matching_order")
}
```

`OpcMatching.status = bid_accepted` 时也写入 `OpcMatchingOrder`。

### 5.5 状态机操作矩阵 (spec §2.2 钉死)

| 当前状态 | fromOpc | toOpc | 系统 |
|---|---|---|---|
| pending | 发起咨询 / 忽略 | 发起咨询 / 忽略 | 失效 (30d) |
| inquiry | 发消息 / 出价 / 拒绝 | 发消息 / 还价 / 拒绝 | 自动关闭 (30d) |
| bid_pending | 等回应 / 改价 | 接受 / 还价 / 拒绝 | 自动撤 (7d) |
| bid_countered | 接受 / 还价 / 拒绝 | 等回应 / 改价 | 自动撤 (7d) |
| bid_accepted | 进入订单 | 进入订单 | 建 OpcMatchingOrder |

cron 任务: 每天扫 matching.createdAt < now-30d AND status IN (pending,inquiry) → expired; createdAt < now-7d AND status = bid_pending → expired。

### 5.6 改动文件

| 文件 | 改动 | 备注 |
|---|---|---|
| `opphub-web/prisma/schema.prisma` | 加 `MatchingStatus` enum + `OpcMatchingBid` + `OpcMatchingOrder` 表, OpcMatching.status 改 enum | - |
| `opphub-web/prisma/migrations/<ts>_matching_state_machine/migration.sql` | 新 migration (active → inquiry 重命名, enum 类型变更) | - |
| `opphub-web/app/api/matchings/[id]/route.ts` | 改 `statusMap.accept`: `active` → `inquiry`; 增加 `statusMap.inquiry_check` (确认当前状态允许) | 现有 |
| `opphub-web/app/api/matchings/[id]/bid/route.ts` | 新 | - |
| `opphub-web/app/api/matchings/[id]/accept-bid/route.ts` | 新 | 跟现有 PATCH accept 区分 (PATCH accept = inquiry, accept-bid = bid_accepted) |
| `opphub-web/app/api/matchings/[id]/counter/route.ts` | 新 | - |
| `opphub-web/app/api/matchings/[id]/bids/route.ts` | 新 (GET only) | - |
| `opphub-web/app/matches/[id]/page.tsx` | 改: 加状态机按钮 (出价 / 接受出价 / 还价 / 拒绝) | 现有页可能已存在 |
| `opphub-web/worker/cron/expire-matchings.ts` | 新 (30d / 7d 过期扫描) | - |

---

## 6. 批 4: 运营基础 (PushLog + 死信 + 导航收尾)

### 6.1 PushLog 表 (spec §5.3)

`opphub-ws` 新表 `push_log` (用 sqlite 简单表, 或复用现有 pending_message 关联):

```prisma
model PushLog {
  id            String   @id @default(cuid())
  messageId     String   @map("message_id")         // pending_message.id
  opcId         String   @map("opc_id")
  channel       String                                // fcm / im / email (本期仅 im)
  status        String                                // success / failed / dead_letter
  attempt       Int      @default(1)
  errorMessage  String?  @map("error_message")
  attemptedAt   DateTime @default(now()) @map("attempted_at")

  @@index([opcId, attemptedAt])
  @@index([status, attemptedAt])
  @@map("push_log")
}
```

在 `opphub-ws/ws-server.js:711` push 成功 + `opphub-ws/ws-server.js:744` ack 超时失败时写入。

### 6.2 死信入口

- 3 次重试后 status = 'dead_letter'
- 后台入口 `/admin/dead-letter` 列死信, 管理员可手动重发 / 标记忽略
- 本期简化: 后台列表先不做, 仅写 PushLog, 死信列表用 SQL 查 (`SELECT * FROM push_log WHERE status = 'dead_letter' ORDER BY attempted_at DESC LIMIT 50`)

### 6.3 导航收尾

`opphub-web/next.config.js`:
```js
redirects: [
  { source: '/match', destination: '/matches', permanent: true },
  { source: '/demands', destination: '/discover?role=buyer', permanent: true },
  { source: '/marketplace', destination: '/discover?role=seller', permanent: true },
]
```

`/match/page.tsx` 内容挪到 `/matches/page.tsx`, `/match` 删除或留 redirect stub。

### 6.4 改动文件

| 文件 | 改动 |
|---|---|
| `opphub-ws/prisma/schema.prisma` | 加 PushLog 表 |
| `opphub-ws/ws-server.js` | push 成功 / 失败时写 PushLog |
| `opphub-web/next.config.js` | 加 redirects |
| `opphub-web/app/match/page.tsx` | 删除或 stub |

**批 4 实施 (2026-07-24)**:
- `opphub-ws/prisma/schema.prisma` PushLog 模型 (push_log 表)
- `opphub-ws/ws-server.js` 3 点写入 (delivered/failed/dead_letter)
- `opphub-web/next.config.js` redirects (已存在, 验证通过)
- `opphub-web/app/match/page.tsx` redirect stub (useRouter().replace('/matches'))
- `opphub-ws/__tests__/push-log.test.js` 集成测试

---

## 7. 数据流总图

```
[discover 页]
  ↓ GET /api/matchings/scores?entryType=ability
  ← candidates (with matchScore, anonymous preview)
[用户点 💬 进入撮合]
  ↓ POST /api/matchings { otherEntryId, message }
  ← { matchingId, status: 'pending' }

[server side]
  ├ 鉴权 → 查 otherEntry → 校验 not self → 找 bestUserEntry
  ├ 频控检查 (24h / 一周 30 / declined 14d)
  ├ prisma.opcMatching.create({ status: 'pending' })
  └ 双方 push (调 opphub-ws POST /push type=match event=match.created)
      ├ toOpcId: { type:'match', event:'match.created', matchingId, otherOpcId: fromOpcId, ... }
      └ fromOpcId: { type:'match', event:'match.created', role:'from', matchingId, otherOpcId: toOpcId, ... }

[opphub-ws POST /push]
  ├ 鉴权 (system trigger 白名单)
  ├ prisma.pendingMessage.create (type='credit')
  └ LPUSH redis opphub:push:queue:opc_xxx
      ↓ [queue worker 100ms RPOP]
      └ WS send → plugin runtime → IM channel (飞书/微信/...)

[用户 B 收推送]
  ↓ 点 IM 卡片 / 打开 /matches/[id]
  ├ MatchingDetail page 显示 (默认匿名)
  ├ 点 "💬 发起咨询" → POST /api/matchings/[id]/inquire { message }
  │   ├ status: pending → inquiry
  │   └ push event=match.inquiry 给 fromOpc
  ├ 聊天 (OpcMatchingMessage) → 谈妥后点 "💰 出价"
  │   └ POST /api/matchings/[id]/bid { amount, termDays, msg }
  │       ├ status: inquiry → bid_pending
  │       ├ 建 OpcMatchingBid
  │       └ push event=match.bid 给对方
  ├ 对方点 "接受" / "还价" / "拒绝"
  │   ├ accept: → bid_accepted, 建 OpcMatchingOrder, push event=match.bid_accepted 给双方
  │   ├ counter: → bid_countered, 建新 OpcMatchingBid (parentBidId), push 给对方
  │   └ decline: → declined, push event=match.declined 给对方
  └ 进入 /orders/[id] (订单详情 + IM + 状态机按钮)
```

---

## 8. 错误处理

| 场景 | 兜底 |
|---|---|
| opphub-ws 不可达 | push 失败降级: `pending_message` 表直接写 (退路), 不阻塞撮合创建 |
| embedding 缺失 | 评分用 baseline (0.4 + dim + geo + industry + recency), 不报错 |
| 频控触发 | 返 429 / 409 + 中文 message + matchingId (如已存在) |
| 撮合已 declined 14d 内 | 返 409 + 中文 message |
| bid amount ≤ 0 | 400 validation error |
| bid termDays ≤ 0 | 400 validation error |
| 撮合 id 不存在 / 不属于 caller | 404 / 403 |
| 撮合状态机非法转移 (e.g. pending 直接 accept) | 409 invalid_state_transition + 当前状态 |

---

## 9. 实施批次与顺序

详见 **§14 实施批次更新** (含批 5 页面 UI, 总 10d)

---

## 10. 风险与缓解

详见 **§15 风险与缓解更新** (含批 5 页面层风险)

---

## 11. 开放问题 (后续明确)

| 问题 | 当前处理 | 待澄清 |
|---|---|---|
| `Demand` / `MatchingRecord` / `Bid` 老模型去留 | 不动, 走 301 | 是否废弃老入口? 何时废弃? 数据保留多久? |
| Payment 表 (escrow/release/refund) | 不在范围 | 阶段 7 钱包做, 跟外部支付网关 (微信支付/支付宝) 一起 |
| `trust_score` 信用分接入匹配评分 | 在批 2 范围 | `OpcTrustScore` (schema:238) 已实现, 批 2 直接接入匹配评分 (0.15 权重) |
| `price_match` 区间匹配 | 不在范围 | `OpcSkillCard.priceMin/Max` 已有, 需扩到 `OpcKnowledgeEntry.parsedFields.priceRange` |
| discover 页匿名 UI | 暂保留 companyName | UI 改版需求 + 用户体验调研 |
| PushLog 死信入口 | 仅写表, 无 UI | 后台 `/admin/dead-letter` 入口 (阶段 6 运营基础设施) |

---

## 12. 关联文档

- `docs/superpowers/specs/2026-07-23-opphub-product-design.md` (产品主架构, 主参考)
- `docs/v3.1-architecture.md` (推送链架构, 批 1 改造依据)
- `docs/runtime-channel-renderer-v31-design.md` (IM 通道渲染, 本次不动)
- `docs/server-schema-v32-design.md` (server schema v3.2, cron 框架可复用)
- `docs/superpowers/plans/2026-07-23-phase5-v1-conflicts-radar.md` (当前 V1 /discover 实施依据, 批 1 改造对照)
- `opphub-web/prisma/schema.prisma` (schema 现状, 批 3 改动)
- `opphub-web/app/api/matchings/route.ts` (现状, 批 1 改造)
- `opphub-ws/ws-server.js` (推送实现, 批 1 鉴权改造 + 批 4 PushLog 写入)

---

## 13. 页面与交互设计

### 13.A 核心产品定位 (钉死)

**撮合单 = 实体, 对话 = 撮合单的核心属性** (舟哥 7/24 拍)

- 每个撮合单**默认带对话流**, 对话不是折叠区
- 对话是撮合单的状态指示器 (未读数 / 最后消息时间 / 最新出价)
- 撮合单的所有操作 (出价 / 接受 / 拒绝) 都通过对话流触发
- 这条贯穿下面所有页面

### 13.B `/matches/[id]` 撮合详情页 (新, **本期核心页面**)

**路由**: `app/matches/[id]/page.tsx`

**布局** (自上而下):

```
┌─────────────────────────────────────────────┐
│ ← 返回   撮合 #M-001   [状态徽章]   ⋯       │  顶部 80px
├─────────────────────────────────────────────┤
│ [对方头像] 对方公司名 · #维度                │
│           📍 城市 · 评分 NN%               │  元数据 60px
├─────────────────────────────────────────────┤
│                                              │
│  [系统消息气泡] 📩 你发起了撮合              │
│  [对方消息气泡] 你好, 我们是做...            │
│  [自己消息气泡] (右对齐)                     │  对话流主体
│  [系统消息] 💰 出价 ¥3000 / 5天交付          │  (占 60% 屏)
│  ...                                         │  滚动到底
│                                              │
├─────────────────────────────────────────────┤
│ [输入框] 2000 字限  [发送]                   │  输入区 80px
├─────────────────────────────────────────────┤
│ [主按钮]  [次按钮]   (随状态变化)            │  操作栏 60px
└─────────────────────────────────────────────┘
```

**状态机 → 操作栏 UI 流转** (核心,本期重点):

| 状态 | 视角 | 主按钮 | 次按钮 | 文本输入 |
|---|---|---|---|---|
| `pending` | 收到方 | `[✅ 接受]` | `[❌ 拒绝]` | 禁用, 但可点接受/拒绝进入 inquiry 后开放 |
| `pending` | 发起方 | (无) | `[取消发起]` | 禁用 |
| `inquiry` | 双方 | `[💰 出价]` | `[⚠️ 拒绝撮合]` | ✅ 启用 |
| `bid_pending` | 出价方 | `⏳ 等待对方回应…` (灰底) | `[撤回出价]` | ✅ 启用 (聊天可继续) |
| `bid_pending` | 对方 | `[✅ 接受出价]` | `[💬 还价]` `[❌ 拒绝]` | ✅ 启用 |
| `bid_countered` | 出价方 | `[✅ 接受还价]` | `[💬 再还价]` `[❌ 拒绝]` | ✅ 启用 |
| `bid_countered` | 还价方 | `⏳ 等待对方回应…` (灰底) | `[撤回出价]` | ✅ 启用 |
| `bid_accepted` | 双方 | `[🎉 进入订单 → /orders/[id]]` | (无) | 禁用, 对话归档 |
| `declined` / `cancelled` / `expired` / `archived` | 双方 | (无) | (无) | 🔒 "撮合已结束, 对话归档" |

**出价 modal** (点击 `[💰 出价]` 触发):

```
┌─────────────────────────────────┐
│  💰 发起出价                    │
├─────────────────────────────────┤
│  金额 (¥)                       │
│  [_______________]              │
│                                  │
│  交付周期 (天)                   │
│  [__]                           │
│                                  │
│  留言 (可选, 200 字)             │
│  [_____________________]         │
│  [_____________________]         │
│                                  │
│  取消          [✅ 提交出价]    │
└─────────────────────────────────┘
```

提交后:
- 写入 `OpcMatchingBid` 表 (status: pending)
- `OpcMatching.status` → `bid_pending`
- 对方收推送 `event: 'match.bid'`
- 对话流插入系统消息: `💰 对方出价 ¥3000 / 5天交付 · [接受出价] [还价] [拒绝]`

**还价 modal**: 同上,但多一行 "参考上一轮出价 ¥3000"

**接受出价 modal** (二次确认, 避免误点):

```
┌─────────────────────────────────┐
│  ✅ 接受出价                     │
├─────────────────────────────────┤
│  对方出价: ¥3000 / 5天交付       │
│                                  │
│  接受后将自动生成订单             │
│  订单创建后双方均无法取消         │
│                                  │
│  取消          [✅ 确认接受]     │
└─────────────────────────────────┘
```

接受后:
- `OpcMatching.status` → `bid_accepted`
- 建 `OpcMatchingOrder` 表 (status: pending)
- 双方收推送 `event: 'match.bid_accepted'`
- 对话流插入系统消息: `🎉 出价已接受, 订单 #O-001 已创建`
- 主按钮变为 `[🎉 进入订单 → /orders/[id]]`

**对话流系统消息格式** (固定模板):

```
[系统] 📩 你发起了撮合
[系统] ✅ 你接受了撮合
[系统] ❌ 你拒绝了撮合
[系统] 🚫 你取消了撮合
[系统] 💰 你出价 ¥3000 / 5天交付
[系统] 💬 你还价 ¥5000 / 7天交付 (上轮 ¥3000)
[系统] ✅ 你接受了对方出价 ¥3000 / 5天交付
[系统] ❌ 你拒绝了对方出价
[系统] 🎉 出价已接受, 订单 #O-001 已生成 → [进入订单]
```

(系统消息存在 `OpcMatchingMessage.text`, 但 `fromOpcId` 是发起方 opcId, 加 `type: 'system'` 字段区分 — schema:287 加 enum `MatchingMessageType: text | system`)

**聊天消息 UX** (沿用 page.tsx 现有):
- 文本消息右对齐自己 (蓝底), 左对齐对方 (灰底)
- 系统消息居中 (灰底, ⓘ 图标)
- 2000 字限, Cmd/Ctrl+Enter 发送
- 发送乐观更新, 失败回滚 + 错误提示
- 进入页面自动 markRead

### 13.C `/matches` 撮合中心 (改)

**现状** (`app/matches/page.tsx`, 524 行):
- 3 tab: 收到 / 发出 / 全部
- 撮合卡 + 内嵌聊天(折叠) + 接受/拒绝/取消按钮
- 智能推荐卡(全部 tab 混在底部)
- 状态标签 pending/active/declined/cancelled

**改造后**:

**筛选维度** (舟哥要求对话内容可筛选):

```
┌─────────────────────────────────────────────┐
│ 🔍 搜索对方公司名...                        │
├─────────────────────────────────────────────┤
│ 方向: [📩 收到 12] [📤 发出 5] [📋 全部 17] │
├─────────────────────────────────────────────┤
│ 对话状态: [💬 有对话 8] [💤 无对话 4] [🔴 仅未读 3] │
├─────────────────────────────────────────────┤
│ 活跃度: [📅 今日] [📆 本周] [⏸ 7d无响应] [🗄 30d无响应] │
├─────────────────────────────────────────────┤
│ 状态: [pending] [inquiry] [bid_pending] [bid_accepted] [declined] │ (multi-select)
├─────────────────────────────────────────────┤
│ 排序: [💬 最后消息 ↓] [⭐ 匹配度 ↓] [🕒 创建时间 ↓] │
└─────────────────────────────────────────────┘
```

(筛选状态保存在 URL `?dir=inbound&conv=with&active=today&status=bid_pending&sort=last_msg`, 刷新保留)

**撮合卡显示**:

```
┌─────────────────────────────────────────────┐
│ [对方头像] 对方公司名              [🔴 3]   │
│             能力「短视频脚本」 ↔ 需求「找达人」 │
│ [inquiry] [inquiry] [bid_pending] [bid_accepted]  ← 状态徽章 (4 选 1)
│ 匹配度 ▓▓▓▓▓▓▓▓░░ 78%                       │
│ 💬 "我们做过 GEO BP, 也对接过..."   3分钟前   │ ← 最后消息预览 + 时间
│ [操作按钮区]                                   │
└─────────────────────────────────────────────┘
```

**5 状态规范接入** (spec §6):

| 状态 | 处理 |
|---|---|
| loading | `<PageSkeleton variant="list">` 3 行骨架 |
| empty | `<EmptyState title="暂无撮合" body="去 /discover 看潜在合作方" primaryCta="去发现" href="/discover" />` |
| error | `<ErrorState code={err.code} message={err.message} retry={reloadAll} />` |
| unauth | 自动跳 `/login?redirect=/matches` |
| 未实名 | 灰度 CTA "立即实名解锁撮合" (banner 顶部) |

**筛选/排序实现**: 客户端本地筛 (matching 列表通常 < 100 条), 不调后端分页。如果量级增长再迁服务端 (`/api/matchings?conv=with&active=today`)。

**未读角标**: 撮合卡右上角红色徽章 + 数字 (`matching.unreadCount`), 同时 TopBar 撮合入口加未读数 (从 `/api/matchings?role=both` 取 `totalUnread`)。

### 13.D `/discover` 发现页 (改,简写)

**改造点**:
1. 撮合 CTA 成功后 modal 文案改: `🤝 撮合已发起 → [💬 进入对话]`(按钮跳 `/matches/[id]`)
2. Modal 显示撮合 ID + 对方公司名 + "对方会在撮合中心收到提醒"
3. 不做匿名化 (spec §4.7 留作后续 UI 改版, 7/24 舟哥拍保持现显示)

**改动文件**: `app/discover/page.tsx:530-555 MatchingResultModal`

### 13.E `/orders` 订单列表 (新,简写)

**路由**: `app/orders/page.tsx`

**布局**:
```
Tabs: [进行中] [已完成] [争议中] [已取消]
列表: 订单号 · 对方公司名 · 金额 · 状态徽章 · 创建时间
       ↓ 点 → /orders/[id]
```

**API**: 复用 `GET /api/orders?role=buyer|seller|both&status=...`, 但 `Order` 是老 Demand 模型专用。本期**新建** `GET /api/matching-orders` (对应 `OpcMatchingOrder` 表), 见 §5。

### 13.F `/orders/[id]` 订单详情 (新,简写)

**路由**: `app/orders/[id]/page.tsx`

**布局**:
```
头部: 订单号 · 金额 · 状态徽章 · 关联撮合 (点跳 /matches/[id])
状态机操作区: 需求方 [付款] [验收] [发起争议] / 供应方 [开始干活] [交付]
对话延续: 复用撮合详情对话组件, history 自动拼接 (撮合对话 + 订单对话 同一 thread)
```

**对话延续实现**: 撮合对话 `OpcMatchingMessage` (matchingId = M-001), 订单对话 `OpcMatchingOrder` 的 chat 复用同一 `matchingId` (订单表存 `matchingId`), 拉对话时 `WHERE matching_id = ?` 一并取。

### 13.G 通知 UX (简写)

- `/dashboard` 加 banner: `🔥 N 个撮合有未读消息 [去查看 →]` (从 `/api/matchings?role=both` 取 `totalUnread`)
- 推送卡片 (飞书/IM) 渲染: 标题 `🤝 撮合通知` + 对方名 + 维度 + `[💬 打开对话]` 按钮 (跳 `/matches/[id]`)
- 推送 schema 已在 §3.4 定, 此处仅前端展示

### 13.H 5 状态规范 (简写)

**通用组件** (新建):
- `app/_components/PageSkeleton.tsx` (variant: list / card / detail)
- `app/_components/EmptyState.tsx` (title / body / primaryCta / secondaryCta)
- `app/_components/ErrorState.tsx` (code / message / diagnostic / retry)

**接入页面**: discover / matches / matches[id] / orders / orders[id] 全部 5 状态。

**错误兜底**:
| 场景 | 兜底 |
|---|---|
| 接口 5xx | retry 3 次 (指数退避) 后报错, 错误存 localStorage, 下次访问恢复 |
| 网络断 | 全局 "网络已断开" banner, 恢复自动消失 |
| 鉴权 401 | 自动跳登录, 登录后回原页 |
| 撮合接口 409 限流 | `alert("太快了, 等 30 秒再来")` |
| 出价 amount ≤ 0 | input 红框 + 提示 |
| bid 失败 | 还原输入, 不乐观更新 |

### 13.I 跳转流总图

```
[/discover] 💬 进入撮合 → modal → [/matches/[id]]
                                          ↓
[/matches] 撮合卡 → 点 → [/matches/[id]]
                          ├ 接受 → status: inquiry → 可发消息
                          ├ 出价 → status: bid_pending → 对方接受/还价/拒绝
                          ├ 接受出价 → status: bid_accepted → 弹窗 [🎉 进入订单]
                          ↓                                                ↓
              [🎉 进入订单] → [/orders/[id]]                                ↓
                              ↓                                            ↓
                          付款 → in_progress → 交付 → 验收 → completed     ↓
                          ↓                                                ↓
                          [/orders?tab=completed]                          ↓
                                                                            ↓
[/dashboard] banner "🔥 N 个撮合有未读" → [/matches?unread=1] ←────────────┘
[飞书/IM 推送] 💬 打开对话 → [/matches/[id]]
```

---

## 14. 实施批次更新 (原 §9)

| 批 | 内容 | 工作量 | 依赖 |
|---|---|---|---|
| 批 1 | 推送管道接通 (根问题) | 1.5d | 无 |
| 批 2 | 评分公式升级 + 频控 + 匿名 | 2d | 批 1 |
| 批 3 | 状态机补全 (inquiry / bid / accept / decline) | 2d | 批 1 |
| 批 4 | 运营基础 (PushLog + 死信 + 导航收尾) | 1.5d | 批 1 |
| **批 5 (新)** | **页面 UI** | **3d** | **批 1, 3** |
| | **B. `/matches/[id]` 详情页 (含对话主体 + 状态机操作栏)** | **1.5d** | |
| | **C. `/matches` 筛选维度 + 5 状态规范** | **0.5d** | |
| | **D-I. `/discover` modal 改 / `/orders` 列表+详情 / 通知 / 跳转流** | **1d** | |

**总: 10d** (原 7d + 批 5 = 3d 页面), 可分 2-3 个 sprint。

**批 5 优先级**: B > C > D > E > F > G > H > I (与舟哥 7/24 拍一致)

---

## 15. 风险与缓解更新 (原 §10)

(原 §10 风险不变, 新增批 5 风险)

| 风险 | 缓解 |
|---|---|
| `/matches/[id]` 对话流复用现有 `ChatThread` 组件, 但操作栏是新加的, 状态机联动复杂 | 先画 wireframe, 拍板后再写; 状态机表 (§13.B) 是唯一真理来源, 前端照表渲染 |
| 撮合详情页路由 `/matches/[id]` 是新加, 现有 `/matches` 内嵌 ChatThread 保留 (过渡期), 两边状态可能不一致 | 本期先把 `/matches/[id]` 做出来, `/matches` 撮合卡点击跳详情, 内嵌 ChatThread 废弃 |
| 筛选维度多, 状态保存 URL 可能太长 | 优先存 cookie/localStorage, URL 只存核心 (dir + unread) |
| `/orders` 路由新建, 跟老 Demand 模型 Order 表有命名冲突 | 新表 `OpcMatchingOrder`, 新路由 `/orders/[id]` 查此表; 老 Order 表路由 `/admin/legacy-orders` (本期不实装) |
| 系统消息 schema 缺 (现有 `OpcMatchingMessage` 只有 fromOpcId/text) | migration 加 enum `MatchingMessageType: text \| system`, 系统消息 fromOpcId = 发起方 opcId + type = system |

---

## 16. Spec 自审 (原 §13)

- ✅ 决策都有理由
- ✅ 5 批之间无耦合, 可分批发布
- ✅ 关键改动引用 file:line
- ✅ 数据流覆盖 discover → 撮合 → 消息 → 订单全链
- ✅ 状态机枚举对齐 spec §2.3
- ✅ 推送管道接通对齐 spec §5.3 + §8.3
- ✅ 评分公式对齐 spec §4.3 (本期实现 4/5, trust_score 已可接入, price_match 留作开放)
- ✅ 频控对齐 spec §4.6
- ✅ 匿名对齐 spec §4.7 (本期 /matches/[id] 实现, discover 页留作开放)
- ✅ 校正现有 endpoint (PATCH accept/decline/cancel + 聊天 + 已读) 已实装, 状态机迁移 active→inquiry 即可
- ✅ trust_score 表已存在, 批 2 直接接入, 不需要新表
- ✅ **页面层: 撮合详情页 (§13.B) 状态机 UI 流转 8 个状态全覆盖, 操作栏动态渲染**
- ✅ **页面层: 撮合中心 (§13.C) 筛选维度含舟哥要求的"对话内容筛选" + 5 状态规范**
- ✅ **核心产品定位: 撮合单 = 对话实体 (§13.A)**
- ✅ **跳转流覆盖 7 个入口 (§13.I)**
- ⚠️ 老 Demand 模型去留留作开放 (scope 限制)
- ⚠️ Payment 表留作开放 (scope 限制)
- ⚠️ trust_score / price_match 留作开放 (依赖其他 spec)
- ⚠️ `/matches/[id]` 路由新建, 现有 `/matches` 内嵌 ChatThread 过渡处理 (本期后期废弃)
- ✅ **批 1 已实装 (2026-07-24)**: 见 §3 末尾 commit 表 + Task 4 端到端验证记录. 推送管道从直接 `pendingMessage.create` 改为走 `opphub-ws POST /push` (system trigger 白名单 + service JWT 双保险)
