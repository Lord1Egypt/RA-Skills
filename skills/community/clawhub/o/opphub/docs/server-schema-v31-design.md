# opphub-server schema v3.1 · 知识库改造设计

> "现在的 公司能力卡片, 是记录到数据库的, 是字段固定的, 但是我要改成开放式的, 整个录入的信息是存到知识库里, 也就是向量存储, 这样就不拘泥于字段"

> **含义**: server schema 改造是 opphub-server 团队活, **不在 opphub skill v3.1 范围**

---

## 0. 文档归属

| 项 | 归属 |
|---|---|
| 本档 (server schema) | opphub-server 团队 |
| opphub skill v3.1 doc | skill 层 (我开干的范围) |
| OpenClaw runtime 渲染层 | runtime 团队 (单独存档) |

---


> "现在的 公司能力卡片, 是记录到数据库的, 是字段固定的, 但是我要改成开放式的, 整个录入的信息是存到知识库里, 也就是向量存储, 这样就不拘泥于字段"

## 2. 与 7/15 蒸馏设计的关系

- **7/15 web P0 蒸馏设计**: `OpcProfile.distilledJson` + `embedding vector(768)` + `lib/distill.ts` LLM 填空字段

---

#### 6.5 schema 改造 (新加 + 弱化)

**新加 `OpcKnowledgeEntry`**:

```prisma
model OpcKnowledgeEntry {
  id              String   @id @default(cuid())
  opcId           String   @map("opc_id")
  sourceType      String   @map("source_type") // rawText / url / upload / auto / manual
  sourceUrl       String?  @map("source_url")
  rawText         String   @map("raw_text") @db.Text
  chunks          Json?    // [{text, start, end, embedding_ref}]
  embedding       Unsupported("vector(768)")?
  embeddingModel  String?  @map("embedding_model")
  embeddingVersion Int?    @map("embedding_version")
  fulltext        Unsupported("tsvector")?  // 全文索引
  distilledTags   String[] @map("distilled_tags") // LLM 抽, 可空, 可自举
  visibility      String   @default("PRIVATE") // PRIVATE / PUBLIC
  createdAt       DateTime @default(now()) @map("created_at")
  updatedAt       DateTime @updatedAt @map("updated_at")
  deletedAt       DateTime? @map("deleted_at")

  opc OpcAccount @relation(fields: [opcId], references: [opcId])

  @@index([opcId, deletedAt])
  @@index([visibility])
  @@map("opc_knowledge_entry")
}
```

**弱化 `OpcProfile`**(字段保留但**不强制填**,作为蒸馏快照):

```prisma
model OpcProfile {
  // 砍: mainSkill, subSkills, experience, cases, priceMin, priceMax, differentiators
  // 留: distilledJson (快照, LLM 蒸馏结果, 可空)
  // 留: embedding + embeddingModel + embeddingVersion (跨 entry 聚合向量)
  // 新加: knowledgeCount Int @default(0)  // 关联多少条 OpcKnowledgeEntry
  // 新加: lastKnowledgeAt DateTime?        // 最近一次入知识库
}
```

**弱化 `OpcSkillCard`**(从"多张字段卡"改成"多 entry 的视图"):

```prisma
// 方案 A: 保留 OpcSkillCard 表, 但字段全是可空, 只作为展示快照
// 方案 B: 直接砍 OpcSkillCard, 改用 OpcKnowledgeEntry 聚合
```

**全文索引 + 向量索引**(§7 决策已钉,7/14 拍):
- pgvector HNSW: `m=16, ef=64`(7/14 拍)
- tsvector: `to_tsvector('simple', rawText)`,GIN 索引
- 检索: `embedding <=> query_embedding` + `fulltext @@ to_tsquery('simple', query_text)`,**完全不需要 JOIN 表**


---

#### 6.6 检索姿势 (matching 时)

```sql
-- 候选 OPC 召回 (Stage 1: 向量召回)
SELECT e.opcId, e.id AS entryId, e.rawText,
       e.embedding <=> $1::vector AS distance,
       e.distilledTags
FROM opc_knowledge_entry e
WHERE e.deletedAt IS NULL
  AND e.visibility = 'PUBLIC'
ORDER BY e.embedding <=> $1::vector
LIMIT 50;

-- 二次过滤 (Stage 2: 全文 + tag 过滤, 不 JOIN 表)
SELECT * FROM (
  -- 上面的结果
) candidates
WHERE candidates.fulltext @@ to_tsquery('simple', $2)
  AND candidates.distilledTags && $3::text[];  -- 任意 tag 命中

-- LLM 精排 (Stage 3: 跟 7/15 设计同)
```

