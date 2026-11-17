# 阶段 5 V1: 冲突解决 + 能力雷达 + 公司画像聚合

> **Agent 实施时按 subagent-driven-development 走 task-by-task**

---

## 0. 边界

**已做 (commit 在 main)**: DB `parsedFields Json?` + `lib/conflicts.ts` + GET API 返 `computeCurrentFields(parsedFields)` + PATCH 接受 `userOverrides`.

**V1 做**: skill 拼 _sources / recharts 雷达 / /knowledge 重写 / /discover 重写含撮合触发 + 详情 modal

**不做**: 时间衰减 / 置信度加权 / HR-CRM 自动同步 / 撮合→交易 / PDF 解析 / 推送 / PUBLIC 过滤 / sources 时间线

---

## 1. 数据契约 (V1)

### `parsedFields` (V1 单 source 简化)
```js
{
  // 顶层 = 用户可见当前值 (computeCurrentFields 实时算)
  companyName, industry:{code,name}, legalPerson, registeredCapital,
  creditCode, teamSize, address, city, businessDescription,
  _sources: {
    [field]: {
      current: <value>,
      userOverride: null | <value>,         // null = 没仲裁
      userOverrideAt: null | ISO,
      candidates: [
        { value, source: "im:msg-uuid", sourceType: "im", ingestedAt: ISO }
      ]
    }
  }
}
```

V1 算法: current = userOverride 优先, 否则 candidates 里 ingestedAt 最新. 无时间衰减无 confidence.

### `opc_matching` 表
```
fromOpcId, toOpcId, fromEntryId, toEntryId, matchScore, status (pending/active/declined/closed), createdAt, updatedAt
```

---

## 2. Tasks

| # | Files | Action |
|---|---|---|
| 1 | skill knowledge-card | extractParsedFields 加 _sources |
| 2 | skill knowledge-submit | 确认传 parsedFields (无改动, 验证) |
| 3 | opphub-web package.json + _components/CapabilityRadar.tsx | 装 recharts, 写雷达组件 (5-8 维, fill 100%) |
| 3.5 | prisma/schema.prisma + api/matchings/route.ts + api/matchings/[id]/route.ts | 加表 + POST + GET |
| 4 | app/knowledge/page.tsx | 重写: 头部画像 + 雷达 + 4 类子卡网格 |
| 5 | app/discover/page.tsx | 重写: 雷达缩略 + 关联理由 + 「进入撮合」CTA (POST + 结果 modal) + 「看完整画像」CTA (详情 modal) |
| 6 | scp + db push + build + restart | Deploy |

---

## Task 1: skill knowledge-card 输出 _sources

**改**: `extractParsedFields(name, rawText, industry)` 同时输出顶层字段 + `_sources`

- 每个顶层字段 (companyName, industry, legalPerson, registeredCapital, creditCode, teamSize, address, city, businessDescription) 都配 1 个 candidate (sourceType="im", source="im:skill-extract:" + ISO 时间戳, ingestedAt=ISO)
- 顶层字段名 + _sources key 保持一致 (避免 computeCurrentFields 跳过)

**Verify**: 跑 node bin/opphub-knowledge-card --name "X" --raw-text "..." --json, parsedFields._sources 应含 9 个 keys (含 companyName/industry 等), 每个 candidates 长度 1

**Commit**: `feat(skill): knowledge-card parsedFields 加 _sources 多源结构`

---

## Task 2: skill knowledge-submit 持续传 parsedFields

**Verify**: 当前 body 已含 `parsedFields: parsedFields ?? undefined` — 无需改动, 验证仍存在

**可能 commit**: `chore(skill): 确认 submit 透传 parsedFields` (如果发现需要修, 不需要则 no commit)

---

## Task 3: recharts + CapabilityRadar

**装**: `npm install recharts --save`

**New file**: `app/_components/CapabilityRadar.tsx`
- Props: `data: [{name, level}]`, `size`, `height`
- Recharts: `RadarChart > PolarGrid, PolarAngleAxis, PolarRadiusAxis (domain 0-1), Radar (dataKey=level, fill=#4f46e5, opacity=0.4)`
- 默认 size=320 height=320

**Commit**: `feat(ui): 装 recharts + CapabilityRadar 组件`

---

## Task 3.5: opc_matching 表 + POST/GET /api/matchings

**Schema**: prisma/schema.prisma 加 `model OpcMatching` (见 §1)
- `OpcAccount` 加两个 relation: `matchingsFrom OpcMatching[] @relation("MatchFrom")` + `matchingsTo OpcMatching[] @relation("MatchTo")`

**db push**: 在容器内 `DATABASE_URL=... npx prisma db push --skip-generate --accept-data-loss`

**Create**: `app/api/matchings/route.ts`
- POST: 接收 `{ otherEntryId, matchScore }`, 鉴权 (JWT) → 查 otherEntry → 校验 not self → 检查去重 (same fromOpc+toOpc status=pending 已存在则复用) → `prisma.opcMatching.create({status:"pending"})` → 返 `{ok, matchingId, status}`
- GET: 接受 `?role=from|to|both` → 列出我的 matchings

**Commit**: `feat(api): opc_matching 表 + POST /api/matchings (撮合触发 + V1 推送占位)`

---

## Task 4: /knowledge 重写

**Replace**: `app/knowledge/page.tsx` 整文件重写, 重点:
- `Suspense` wrap + `KnowledgeInner` 子组件 (避免 useSearchParams 警告)
- fetch `/api/knowledge?opcId=me`, `entries: EntryShape[]`
- 取第一条 ability/downstream entry 的 parsedFields 做 profile (companyName/industry/teamSize/city/legalPerson/registeredCapital/businessDescription)
- 数据不分组, 4 类子卡用 `grouped = useMemo(...)` 归集, `TAB_ORDER = ['ability','downstream','upstream','peer']`
- 能力雷达: 取 grouped.ability.slice(0, 8).map(e => ({name: e.entryDimension, level: 0.7})) — V1 固定 0.7
- Header card: 公司名 + 元信息 + 业务描述
- 4 类子卡网格: 每类独立 section, 卡片展示 entryDimension
- 卡片点击跳 `/knowledge/${e.id}` (DetailModal 留作后续)
- 不再做 modal (详情/编辑/删除) — V1 只搭页面结构, modal 留作后续
- 空状态: 提示去 IM @偶合 录入

**Commit**: `feat(knowledge): /knowledge 重写为公司画像 + 能力雷达 + 4 类子卡网格`

---

## Task 5: /discover 重写

**Replace**: `app/discover/page.tsx` 整文件

**核心**:
- `Suspense` wrap + `DiscoverInner`
- 读 sp `role` (buyer/seller, default buyer)
- 我的 type: `role==='buyer' ? downstream : ability`
- 候选 type: `role==='buyer' ? ability : downstream` (V1: 候选来自自己的另一个 type, 同 OPC 内, 因为 PUBLIC 还没实装)
- `calcMatchScore(myType, otherType, ingestedAt)`:
  - ability↔downstream: 0.9
  - 其他: 0.5-0.7
  - 7d 内加权 +0.1
- 渲染每张卡片: 公司名 + 关联度 badge + 雷达缩略 (每 entry 的 _sources 字段名, level 0.7) + 关联理由 + 双 CTA
- CTA「进入撮合」: `startMatching(entry)` — fetch POST /api/matchings, 弹 MatchingResultModal
- CTA「看完整画像」: `setDetailEntry(entry)` — 弹 DetailModal

**Modal 组件** (放在 page.tsx 末尾):
- `DetailModal`: 弹窗内显示公司基本信息 + 业务描述 + 能力雷达 + rawText (折叠 details)
- `MatchingResultModal`: 显示「撮合已发起, 待对方回应」状态, success 时含绿色提示「撮合中心/IM/出价/订单 将在下阶段实装」

**states**: detailEntry, matchingResult, related state setters

**Commit**: `feat(discover): 重写 - 雷达缩略 + 关联理由 + 撮合 CTA + 详情 modal`

---

## Task 6: Deploy + 烟测

**scp**: package.json, package-lock.json, prisma/schema.prisma, app/_components/CapabilityRadar.tsx, app/knowledge/page.tsx, app/api/matchings/**, app/discover/page.tsx

**Container**:
```bash
docker exec opphub-web sh -c "cd /app && npm install recharts --save 2>&1 | tail -3"
docker exec opphub-web sh -c "cd /app && DATABASE_URL=... npx prisma db push --skip-generate --accept-data-loss 2>&1 | tail -3"
docker exec opphub-web sh -c "cd /app && rm -rf .next && npm run build 2>&1 | tail -5"
docker restart opphub-web
```

**烟测**:
- /knowledge 200
- /discover 200
- 跑 skill 录入上海睿驰嘉禾 → 数据库 parsedFields._sources 写入
- POST /api/matchings 在 curl 测能创建

**Tag**: `phase-5-v1-conflicts-radar`

---

## 流程图

```
/discover → 看卡片 → 点「💬 进入撮合」 
  → POST /api/matchings (V1 推送占位) 
  → 弹 MatchingResultModal (撮合已发起, 待对方回应)
  → 提示下阶段

点「👀 看完整画像」 
  → 弹 DetailModal (公司画像 + 雷达 + rawText)
```
