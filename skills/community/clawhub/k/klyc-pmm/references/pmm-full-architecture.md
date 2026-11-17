# PMM 全量架构（14层 + 四子业务）

## 三层十一表

```
                      klyc_memories
                      ══════════════════════
                      主记忆表（单表，按 user_id 行级隔离）
                      ├─ 内容层: title, content, content_hash, content_preview
                      ├─ 分类层: domain, category, tags
                      ├─ 质量层: importance, quality_score, is_essence, memory_tier
                      ├─ 安全层: is_encrypted, is_public, token_cost
                      ├─ 生命周期: is_deleted, deleted_reason, distill_merged_to,
                      │           last_accessed_at, expires_at
                      └─ 统计层: access_count, contributor_count

   ┌──────────────┬──────────────┬──────────────┬──────────────┐
   │ 1:1          │ 1:N          │ 1:N          │ 1:1          │
   ▼              ▼              ▼              ▼
embeddings     audit_log      contributors   quality_scores
══════════     ═════════      ════════════   ══════════════
memory_id      memory_id      memory_id      memory_id
embedding_json action ──┐     user_id        score_completeness ← BERTScore
assertion_offsets ─┐   │     (联合贡献者)    score_density      ← 断言拆分器
has_assertions    │   │                     score_freshness    ← 时间衰减
                  │   │   old_value (JSON)  score_citation     ← 引用计数
                  │   │   new_value (JSON)  score_verification ← 跨体验证
                  │   │   changed_by ──────► klyc_users         score_consistency  ← NLI
                  │   │   changed_via       overall_score (0-100)
                  │   │   ip_address        grade (S/A/B/C/D)
                  │   │   created_at
                  │   │
                  │   └── action ∈ {create, update, delete, merge,
                  │                 restore, decay, archive, lock}
                  │
                  └── 子句级蒸馏预留: [{start:N, end:M, text:"..."}, ...]

   ┌──────────────┬──────────────┐
   │ M:N          │ 1:N          │
   ▼              ▼
conflicts        reactions
═════════        ═════════
memory_id        memory_id
conflict_memory_id  user_id
scope ────────── reaction (1=up, 0=down)
│  ├─ internal   created_at
│  └─ cross_body
conflict_type    access
similarity       ══════
detail (JSON)    owner_id
status           accessor_id
arbitrator_id    can_read / can_write
resolution_note
        │
        │ 仲裁后按 topic_hash 聚合
        ▼
   consensus
   ═════════
   topic_hash (BGE-M3 聚类)
   memory_ids (JSON[])
   user_ids (JSON[])
   consensus_content
   consensus_score
   status ∈ {pending, partial, consensus, deadlock}
```

## 三层职责

| 层 | 表 | 职责 |
|:--:|------|------|
| **核心** | `klyc_memories` | "这条记忆是什么？" |
| **加工** | embeddings, quality_scores, conflicts, consensus | "有多相似？质量如何？有矛盾吗？共识是什么？" |
| **追踪** | audit_log, contributors, access, reactions | "谁动了？谁在看？谁认可？" |

## 关键设计决策


每个 AI 体的记忆存在独立表。`getMemoriesTable($userId)` 动态路由。跨体查询走 `klyc_memory_conflicts.scope='cross_body'` + BGE-M3 语义桥。

**2. quality_score 主表快照 + 独立表明细双写**
主表存 `decimal(5,2)`（查询无需 JOIN），独立表 `klyc_memory_quality_scores` 存六维明细（分析用）。`klyc_reconcile_quality.py` 每日 4:30 对账修复不一致。

**3. assertion_offsets 预留不激活**
`has_assertions=0` 默认。5 信号 ≥3 亮起时批量 `/split` → 子句级 embed。零成本等待。

**4. scope 字段复用 conflicts 表**
`internal` 同体冲突 / `cross_body` 跨体冲突 → 同表不同 scope。避免维护两张冲突表。

**5. 审计日志外挂式**
`auditLog()` 函数手动写入，在每次状态变更后立即调用。90 天自动清理。`klyc_memory_create.php` 已注入审计钩子，覆盖率从创建点开始自动爬升。

## 14 层蒸馏管道

| 阶段 | 环节 | 工具 |
|:--:|------|------|
| **基础（4）** | 寻踪 | BGE-M3 + BM25 hybrid |
| | 织网 | BERTopic 自动分类 |
| | 入库 | Qdrant cosine 索引 |
| | 还原 | 昆仑令容灾恢复 |
| **质量（6）** | 鉴伪 | cross_body NLI 对比 |
| | 归并 | BGE-M3 ≥0.85 合并 |
| | 断矛 | NLI contradiction 检测 |
| | 系脉 | BGE-M3 关联钩子 |
| | 修订 | BERTScore 保真度 |
| | 追本 | 审计日志 before/after |
| **安全（3）** | 审计 | audit_log 自动留痕 |
| | 加密 | AES-256-GCM |
| | 容灾 | 五域递进容灾 |
| **进化（4）** | 炼金 | 子句级拆分 |
| | 提纯 | BERTScore 评估 |
| | 通变 | 跨体共识仲裁 |
| | 取舍 | 生命周期衰减归档 |

## 9 工具 × 14 层覆盖矩阵

| | 寻踪 | 织网 | 入库 | 还原 | 鉴伪 | 归并 | 断矛 | 系脉 | 修订 | 追本 | 审计 | 加密 | 容灾 | 炼金 | 提纯 | 通变 | 取舍 |
|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| BGE-M3 | ✅ | ✅ | | | | ✅ | | ✅ | | | | | | | | | |
| Reranker | ✅ | | | | | | | | | | | | | | | | |
| BERTScore | | | | | | | | | ✅ | | | | | | ✅ | | |
| NLI | | | | | ✅ | | ✅ | | | | | | | | | ✅ | |
| 断言拆分 | | | | | | | | | | | | | | ✅ | ✅ | | |
| Qdrant | ✅ | ✅ | ✅ | | | | | | | | | | | | | | |
| BM25 | ✅ | | | | | | | | | | | | | | | | |
| spaCy | | ✅ | | | ✅ | | | | | | | | | ✅ | | | |
| BERTopic | | ✅ | | | | | | | | | | | | | | | |

## 子句级升级路径

```
当前状态                               升级后
has_assertions=0                       has_assertions=1
整条 content → 单个 embed              content → N 个 assertions → N 个 embeds
跨体匹配: memory vs memory            跨体匹配: assertion vs assertion
冲突粒度: 记忆级                      冲突粒度: 句子级
```

触发条件（5 信号 ≥3 亮起）：
- memory 总量 >10K
- cross_body 冲突 >100
- consensus deadlock >10
- quality_score 标准差 >15
- NLI contradiction 比例 >5%

## 运维 cron

| 时间 | 脚本 | 职责 |
|------|------|------|
| 每日 2:05 | klyc_distill_cron.php | BGE-M3 粗筛 → DeepSeek 蒸馏 |
| 每日 2:00 | klyc_auto_tag_domain.php | 无域记忆自动归类 |
| 每日 3:00 | klyc_qnp_backup.py | QNP 全量备份 |
| 每日 4:00 | klyc_a2a_logger.py | A2A 日志清理 |
| 每日 4:30 | klyc_reconcile_quality.py | quality_score 双写对账 |
| 每日 6:00 | klyc_distill_qa.php | QA 蒸馏 |
| 周日 3:00 | klyc_memory_lifecycle.php | 衰减→归档→评分→冲突检测→审计清理 |
| 周日 4:00 | klyc_l2_detect.php | 双阈值冲突检测 |
| 周日 4:00 | klyc_table_cleanup.py | 旧分表归档清理（迁移后7天DROP） |
| 周日 5:05 | yaochi_cross_distill.sh | 交叉蒸馏 |

## 服务端口

| 服务 | 端口 | 用途 |
|------|:--:|------|
| BGE-M3 | 8766 | 语义搜索 / 向量嵌入 |
| BGE Gateway | 8765 | BGE-M3 稳定性代理 |
| BGE-Reranker | 8770 | 搜索结果重排序 |
| eval-server | 8769 | BERTScore + NLI + 断言拆分 |
| Qdrant | 嵌入模式 | 向量索引 / 聚类（无端口） |
