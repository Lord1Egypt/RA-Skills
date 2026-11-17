# server schema v3.2 设计 · idempotent ingest

>
> 关联 workboard: `v3.3-skill-server-separation-2026-07-20` (id=bc34d33f-...)
>
> **跟 v3.1 关系**: v3.1 schema 弱化了 OpcProfile/OpcSkillCard，加了 OpcKnowledgeEntry;
> v3.2 在 OpcKnowledgeEntry 基础上加 idempotent ingest 能力，**不动 v3.1 已拍的结构**。

---



1. **无去重**：server `OpcKnowledgeEntry.create()` 直接 create，0 个 unique constraint（除 entry.id 主键）
   - 同 OPC 同 rawText 提交 2 次 → 2 条 entry

2. **无幂等键**：改一个错别字只能新建 entry，原 entry 还在
   - 没 `idempotencyKey` 概念
   - 没 `contentHash` 概念

3. **无冲突检测**：录入有矛盾字段时静默入库
   - 没版本管理 / source 优先级 / 时间戳覆盖策略

---


- **P1**: skill = 采集者 + 翻译者，只产 rawText。**不做任何去重 / 冲突判断 / 版本管理**
- **P2**: server = 仓库 + 处理器，做去重 / 冲突检测 / 版本管理 / 蒸馏 / 嵌入 / 召回
- **P3**: 幂等性 + 冲突处理都在 server 端按 **content-addressable + idempotencyKey** 双重保险

---

## 三、Schema 改造 (最小)

### 3.1 OpcKnowledgeEntry 加字段

```prisma
model OpcKnowledgeEntry {
  // 现有字段 (v3.1) - 不动
  id           String  @id @default(cuid())
  opcId        String  @map("opc_id")
  sourceType   String  @map("source_type") // rawText / url / upload / auto / manual
  sourceUrl    String? @map("source_url")
  rawText      String  @map("raw_text") @db.Text
  status       String  @default("pending") // pending / processing / done / failed
  chunkSummary Json?   @map("chunk_summary")
  embeddingModel   String? @map("embedding_model")
  embeddingVersion Int?    @map("embedding_version")
  distilledTags String[] @default([]) @map("distilled_tags")
  visibility    String   @default("PRIVATE")
  retryCount Int     @default(0) @map("retry_count")
  lastError  String? @map("last_error")
  createdAt DateTime  @default(now()) @map("created_at")
  updatedAt DateTime  @updatedAt @map("updated_at")
  deletedAt DateTime? @map("deleted_at")

  
  // idempotencyKey: SHA256(opcId + entryType + entryDimension)
  //   - 同 OPC 同 type+dimension → 同 key → server 走 upsert 路径
  //   - 改 rawText (改一个错别字) → contentHash 变但 key 不变 → server 比 hash
  idempotencyKey  String? @map("idempotency_key")
  
  // contentHash: SHA256(rawText) 当前内容指纹
  //   - 用来判断 rawText 是否真变了
  contentHash     String? @map("content_hash")
  
  // entryType + entryDimension: skill 拆出来的 4 类卡 (ability/upstream/downstream/peer) + 维度名
  //   - 这 2 个字段是去重的最低必要锚点, 不属于"过度字段化"
  //   - skill knowledge-card 拆出来直接传过来, server 不解析 rawText 前缀
  entryType       String? @map("entry_type")        // ability / upstream / downstream / peer
  entryDimension  String? @map("entry_dimension")   // 达人营销 / KOL 资源 / 品牌方 / ...
  
  // previousEntryId: 软链 (被覆盖的旧 entry), 保留 history
  //   - 跟 git 同款: 老 entry 标 supersededAt, 新 entry previousEntryId 链回老 entry
  //   - 召回时不查 supersededAt != null 的 entry
  previousEntryId String? @map("previous_entry_id")
  supersededAt    DateTime? @map("superseded_at")   // 非 null 即被新 entry 取代
  
  opc    OpcAccount          @relation(fields: [opcId], references: [opcId])
  chunks OpcKnowledgeChunk[] @relation("EntryChunks")
  
  @@unique([opcId, idempotencyKey])                    // 幂等唯一键
  @@index([opcId, entryType, entryDimension])          // 检索
  @@index([opcId, deletedAt])                          // 现有
  @@index([supersededAt])                              // 召回过滤
}
```



**v3.2 加的字段**:
| 字段 | 是否破坏"开放式" |
|---|---|
| `idempotencyKey` | ❌ 不破坏。skill 算 hash 传过来, server 不解析内容 |
| `contentHash` | ❌ 不破坏。纯 hash, 不存业务语义 |
| `previousEntryId` + `supersededAt` | ❌ 不破坏。跟 git 同款, 不删 history |

**核心**: rawText 仍然全量存 (这是 12:58 拍的精神), 加的结构化字段都是**辅助字段** (去重 + 索引 + 版本链), 不替代 rawText。

---

## 四、接口改造

### 4.1 新接口: `POST /api/knowledge/ingest` v2 (idempotent)

**位置**: `/app/api/user/knowledge/ingest/route.ts` (现有 v1 接口保留, 加 v2 路由或加 query param `?v=2`)

**request body**:
```json
{
  "opcId": "opc_1hz6wsjrmt1s",
  "rawText": "睿驰嘉禾 · 能力卡片 · 达人营销\n\n(证据: rawText 包含 \"达人营销\")\n...",
  "entryType": "ability",
  "entryDimension": "达人营销",
  "idempotencyKey": "sha256_hash",
  "contentHash": "sha256_hash"
}
```

**response 4 种**:
```json
// 1. 新增成功
{ "ok": true, "action": "created", "entryId": "cmxxx", "chunkCount": null, "status": "pending" }

// 2. 幂等命中 (rawText 没变)
{ "ok": true, "action": "no_change", "entryId": "cmxxx", "message": "rawText 与已有 entry 完全一致" }

// 3. 软链覆盖 (rawText 变了但无关键字段冲突)
{ 
  "ok": true, 
  "action": "soft_chain_override", 
  "entryId": "cmyyy",                    // 新 entry
  "previousEntryId": "cmxxx",            // 被取代的旧 entry
  "supersededEntry": { "id": "cmxxx", "supersededAt": "..." }
}

// 4. 冲突返报告 (rawText 变了 + 关键字段冲突, 不入库, 等用户拍)
{ 
  "ok": false, 
  "conflict": true, 
  "conflictReport": {
    "entryId": "cmxxx",                  // 已有 entry
    "diffType": "key_field_conflict"     // vs "incremental_addition"
  }
}
```

### 4.2 实现逻辑 (server 端伪代码)

```typescript
// app/api/user/knowledge/ingest/route.ts v2
export async function POST(req: NextRequest) {
  const opcId = getOpcId(req);
  if (!opcId) return unauthorized();
  
  const { rawText, entryType, entryDimension, idempotencyKey, contentHash } = await req.json();
  if (!rawText || !idempotencyKey || !contentHash) return missingArgs();
  
  // 1. 查 unique
  const existing = await prisma.opcKnowledgeEntry.findUnique({
    where: { opcId_idempotencyKey: { opcId, idempotencyKey } }
  });
  
  // 2. 不存在 → 直接 create
  if (!existing) {
    const entry = await prisma.opcKnowledgeEntry.create({
      data: { opcId, rawText, entryType, entryDimension, 
              idempotencyKey, contentHash, status: 'pending' }
    });
    return { ok: true, action: 'created', entryId: entry.id };
  }
  
  // 3. 存在 → 比 contentHash
  if (existing.contentHash === contentHash) {
    // rawText 没变, 静默幂等命中
    return { ok: true, action: 'no_change', entryId: existing.id };
  }
  
  // 4. contentHash 变 → 比 rawText 关键字段
  const diff = diffRawText(existing.rawText, rawText);
  
  if (diff.hasKeyFieldConflict) {
    // 关键字段冲突 → 返 conflictReport, 不入库
    return { 
      ok: false, 
      conflict: true, 
      conflictReport: {
        entryId: existing.id,
        oldRawText: existing.rawText,
        newRawText: rawText,
        conflictFields: diff.conflictFields,
        diffType: 'key_field_conflict'
      }
    };
  }
  
  // 5. 无关键字段冲突 → 软链覆盖
  // 5a. 老 entry 标 superseded
  await prisma.opcKnowledgeEntry.update({
    where: { id: existing.id },
    data: { supersededAt: new Date() }
  });
  // 5b. 新 entry, previousEntryId 链回老 entry
  const newEntry = await prisma.opcKnowledgeEntry.create({
    data: { 
      opcId, rawText, entryType, entryDimension, 
      idempotencyKey, contentHash, 
      previousEntryId: existing.id,
      status: 'pending'
    }
  });
  return { 
    ok: true, 
    action: 'soft_chain_override',
    entryId: newEntry.id,
    previousEntryId: existing.id,
    supersededEntry: { id: existing.id, supersededAt: new Date().toISOString() }
  };
}
```

### 4.3 冲突检测算法 `diffRawText`

```typescript
// lib/diff-raw-text.ts
function diffRawText(oldText: string, newText: string) {
  // 1. 提取关键字段 (正则 + 简单启发式, 不调 LLM)
  const oldFields = extractKeyFields(oldText);
  const newFields = extractKeyFields(newText);
  
  // 2. 比对关键字段
  const conflictFields: string[] = [];
  for (const key of ['legal_person', 'registered_capital', 'business_direction', 'industry']) {
    if (oldFields[key] && newFields[key] && oldFields[key] !== newFields[key]) {
      conflictFields.push(`${key}: ${oldFields[key]} → ${newFields[key]}`);
    }
  }
  
  // 3. 关键字段冲突 vs 增量补充
  const hasKeyFieldConflict = conflictFields.length > 0;
  
  return { 
    hasKeyFieldConflict, 
    conflictFields,
    diffType: hasKeyFieldConflict ? 'key_field_conflict' : 'incremental_addition'
  };
}

// 简单启发式提取关键字段 (不调 LLM, 性能优先)
function extractKeyFields(rawText: string) {
  const fields: Record<string, string> = {};
  
  const legalPersonMatch = rawText.match(/法[定]?人[::]?\s*([^\s,，;；\n]+)/);
  if (legalPersonMatch) fields.legal_person = legalPersonMatch[1];
  
  if (bossMatch) fields.legal_person = bossMatch[1];
  
  // 注册资本
  const capitalMatch = rawText.match(/注册资[本金][::]?\s*([0-9,，.]+\s*[万亿]?)/);
  if (capitalMatch) fields.registered_capital = capitalMatch[1];
  
  // 业务方向 (取第一条)
  const businessMatch = rawText.match(/业务方向[::]?\s*([^\n]+)/);
  if (businessMatch) fields.business_direction = businessMatch[1];
  
  return fields;
}
```

### 4.4 召回过滤改动 (search 路由)

```typescript
// app/api/user/knowledge/search/route.ts 改动
const entries = await prisma.opcKnowledgeEntry.findMany({
  where: { 
    opcId, 
    deletedAt: null,
    supersededAt: null,  // ← 新加: 召回时不查被取代的 entry
  },
  // ... 其他
});
```

---

## 五、Skill 端改动 (v3.3 skill 范围)

### 5.1 新加 `bin/opphub-knowledge-submit.js`

**职责**: 把 cards 提交给 server, 接收 conflictReport, **不做任何判断**

```javascript
#!/usr/bin/env node
// bin/opphub-knowledge-submit.js · v3.3.0
// 
// 本 bin 纯转发 + 透传 server 响应
//
// 输入: cards.json (knowledge-card 输出)
// 输出: { submitted: [...], deduplicated: [...], conflicts: [...] }

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { readToken } from "../lib/opphub-plugin-client.js";

const API_BASE = "https://api.opphub.ruiplus.cn";

function sha256(s) {
  return createHash("sha256").update(s, "utf8").digest("hex");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cards = JSON.parse(readFileSync(args.cards, "utf8"));
  
  // 拿 token (plugin = source of truth, 14:21 拍)
  const tokenDoc = await readToken();
  const accessToken = tokenDoc?.access_token;
  if (!accessToken) {
    return out({ ok: false, error: "no_token", message: "需要先偶合登录" });
  }
  
  // 从 token 解 opcId (skill 不需要 opphub-server 二次确认)
  const opcId = decodeJwt(accessToken).opcId;
  
  const results = { submitted: [], deduplicated: [], conflicts: [] };
  
  for (const card of cards) {
    const idempotencyKey = sha256(`${opcId}|${card.type}|${card.dimension}`);
    const contentHash = sha256(card.text);
    
    const resp = await fetch(`${API_BASE}/api/knowledge/ingest`, {
      method: "POST",
      headers: { 
        "Authorization": `Bearer ${accessToken}`, 
        "Content-Type": "application/json" 
      },
      body: JSON.stringify({
        opcId, 
        rawText: card.text, 
        entryType: card.type, 
        entryDimension: card.dimension, 
        idempotencyKey, 
        contentHash
      })
    });
    const data = await resp.json();
    
    if (data.ok && data.action === "no_change") {
      results.deduplicated.push({ cardIndex: card.index, entryId: data.entryId });
    } else if (data.ok) {
      // created 或 soft_chain_override 都算 "submitted"
      results.submitted.push({ 
        cardIndex: card.index, 
        entryId: data.entryId,
        action: data.action,
        previousEntryId: data.previousEntryId || null
      });
    } else if (data.conflict) {
      results.conflicts.push({ 
        cardIndex: card.index, 
        conflictReport: data.conflictReport 
      });
    }
  }
  
  out({
    ok: true,
    opcId,
    summary: {
      submitted: results.submitted.length,
      deduplicated: results.deduplicated.length,
      conflicts: results.conflicts.length
    },
    submitted: results.submitted,
    deduplicated: results.deduplicated,
    conflicts: results.conflicts,
    nextStep: results.conflicts.length > 0 
      ? "用 bot.skillApi.askInteractive 让用户拍冲突项" 
      : "全部成功, 跑 knowledge-match"
  });
}

main().catch(e => out({ ok: false, error: e?.message ?? String(e) }));
```

### 5.2 改 `bin/opphub-knowledge-ingest-batch.js`

**改动**: 删"循环调 knowledge-add"的逻辑, 改成"调 submit"

```javascript
for (const card of cards) {
  await opphub-knowledge-add --raw-text "$card.text" --source-type auto
}

// 新逻辑 (v3.3)
opphub-knowledge-submit --cards cards.json
```

ingest-batch 变成纯编排入口 (不做实际提交), 实际提交逻辑在 submit bin。

### 5.3 不动的部分 (skill 端)

- ✅ `knowledge-card` 不动 — 仍然按 MCN/SaaS 模板拆 card
- ✅ `knowledge-discover` 不动 — 仍然产 queryPlan / 验 rawText
- ✅ `knowledge-search` 不动 — 召回接口跟 server 同步过滤 superseded
- ✅ `knowledge-relate` 不动 — xls 解析逻辑

---

## 六、Bot 端流程改造 (v3.3)

按 SKILL.md §录入公司流程 阶段 4-5，bot 拿到 `knowledge-submit` 的结果:

```
bot 给你看:
📋 录入睿驰嘉禾 · 结果报告

✅ 新提交 7 条
🔁 已有 3 条 (跳过)
⚠️ 冲突 1 条 (要你拍):
  - 能力卡片 · 虚拟人 IP 孵化
    老: 数字人形象设计
    新: 虚拟主播代运营
    冲突字段: 业务描述

回 "保留旧的" / "用新的" / "跳过"
```

**bot 走 IntentMessage**:
- `askInteractive` 列出冲突项 + 让用户点选
- 用户选择后, bot 再调一次 submit (不传冲突项的 cards, 或传 `forceOverride: true`)

**冲突覆盖流程**:
```
用户: 用新的
bot: 收到, 重新提交 1 条 (跳过冲突检测)
bot 调: opphub-knowledge-submit --cards cards.json --force-override-conflict --json
server: 跳过冲突检测, 强制 soft_chain_override
```

---

## 七、部署 & 测试


1. ✅ **本地 dev migrate** (不部署 ECS)
2. ✅ server 端 schema 改造 + 接口实现 (本地 dev server)
3. ✅ skill 端 submit + ingest-batch 改造 (本地开发)

### 7.2 本地 E2E 测试 (mock server)

```bash
# 1. 启本地 mock server
node tests/mock-knowledge-server.js &

# 2. 跑 skill 端 (用本地 mock URL)
OPPHUB_API_BASE=http://localhost:4001 bin/opphub knowledge-submit --cards /tmp/cards.json

# 3. 验证 4 种响应:
#    - 新增成功 (action: created)
#    - 幂等命中 (action: no_change)
#    - 软链覆盖 (action: soft_chain_override)
#    - 冲突报告 (conflict: true)
```

### 7.3 回滚

- server schema 改造加字段是**可空**的 (idempotencyKey? contentHash? entryType? entryDimension? previousEntryId? supersededAt?)
- 老 entry 没这 6 个字段 → 不影响老流程
- 新 entry 没 idempotencyKey → 走"非幂等路径" (跟 v3.1 行为一致)
- **回滚安全**: 直接撤 server 代码, schema 不动

---

## 八、不动的事 (反复钉的纪律)

- ❌ 不动 plugin 仓 (plugin-cli-cleanup-2026-07-20 单独 backlog)

---

## 九、关联文档

- **设计稿 (本文)**: `workspace/skills/opphub/docs/server-schema-v32-design.md`
- **v3.1 设计稿**: `workspace/skills/opphub/docs/server-schema-v31-design.md` (平行, 不冲突)
- **v3.1 架构**: `workspace/skills/opphub/docs/v3.1-architecture.md`
- **运行时渲染层**: `workspace/skills/opphub/docs/runtime-channel-renderer-v31-design.md` (不动)
- **workboard 卡**: `v3.3-skill-server-separation-2026-07-20` (id=bc34d33f-...)
- **MEMORY 红线**: `~/.openclaw/workspace-dev/MEMORY.md` §v3.3 backlog

---

## 十、下次同样场景

