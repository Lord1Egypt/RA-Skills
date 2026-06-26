---
name: index-optimization
description: 针对指定表或集合做查询模式分析、可复用索引设计与 explain 迭代验证。支持两种优化模式：默认全量模式（定位该表/集合所有查询）与单查询模式（用户指定某条查询时，仅分析该查询并查询数据库现有索引）；支持两种执行确认模式：需确认模式与免确认模式。
---

# 索引优化

## 概述

面向单表或单集合执行端到端索引优化：先定位全部相关查询并给出代码位置，再按数据库类型设计可复用索引，最后通过 explain 循环验证，直到达到预期索引命中。

## 必要输入

执行前收集以下信息：
- 优化模式（可选）：
  - 不指定：`全量模式`（默认，沿用现有逻辑）
  - 指定某条查询：`单查询模式`
- 执行确认模式（可选）：
  - 不指定：`免确认模式`（默认，无需等待用户确认，可直接执行创建/删除索引）
  - 指定：`需确认模式`（执行创建/删除索引前必须等待用户确认）
- 表名或集合名（必填）
- 数据库类型与主版本（MySQL/TiDB/PostgreSQL/MongoDB；未知时默认 MySQL 8）
- explain 执行环境（优先 dev/sit）
- 单查询模式下，额外需要：
  - 目标查询语句（必填）
  - 可选：该查询代码位置（`path:line`）

若数据库类型缺失，明确写出一个假设后继续执行。

## 必需流程

按顺序执行，不跳步。

### 1) 选择模式并收集查询输入

#### 全量模式（默认）
1. 先执行查询定位脚本：
   - `python3 $CODEX_HOME/skills/index-optimization-skill/scripts/collect_table_queries.py --table <table_or_collection_name> --repo-root <repo_root>`
2. 必要时手工补充 grep：
   - SQL：`rg -n --no-heading -S "<name>|query\\.|\\.Table\\(" apps pkg docs`
   - Mongo：`rg -n --no-heading -S "<name>|Collection\\(|\\.find\\(|\\.aggregate\\(|\\.explain\\(" apps pkg docs`
3. 所有查询证据都必须保留代码跳转位置，格式为 `path:line`。
4. 面向用户输出时，代码位置必须使用可点击 Markdown 链接：
   - 标准格式：`[path:line](/absolute/path/to/file#Lline)`
   - 其中路径必须是绝对路径，且带行号锚点 `#L<line>`。

#### 单查询模式（指定某条查询）
1. 不查找其他查询，只保留用户指定的目标查询。
2. 必须先查询数据库当前已有索引（SQL `SHOW INDEX` / `pg_indexes`；Mongo `getIndexes()`）。
3. 基于“目标查询 + 现有索引”进入后续步骤。

### 2) 汇总查询模式

将输入查询按访问模式分组：
- 点查：单行/少量行等值条件
- 范围/分页：`>`, `<`, `BETWEEN`, `ORDER BY ... LIMIT`
- 关联查询：JOIN 键与连接方向
- 写路径：`UPDATE/DELETE` 条件
- 可选过滤：低选择性列（如 `status/is_del/type`）

单查询模式下，仅分析该目标查询，不扩展到其他查询。

### 3) 按数据库类型设计可复用索引

使用 `references/index-rules.md` 的数据库规则。
- 先用最少索引覆盖最高频的共享模式。
- 优先一个可复用复合索引，避免大量重叠索引。
- 每个候选索引都要输出：
  - DDL
  - 覆盖的查询分组
  - 代码使用位置（可点击链接：`[path:line](/absolute/path/to/file#Lline)`）
  - 预期 EXPLAIN 目标（`key`、`type`、`rows`、`Extra`/执行计划节点）

### 4) 变更前给出依据（按执行确认模式处理）

在创建/删除索引前，必须先输出以下内容：
1. 变更类型（新增/删除/替换索引）。
2. 变更依据（对应查询模式、代码位置、explain 证据、预期收益）。
3. 风险评估（写入开销、锁影响、回滚方案）。
4. 待执行语句（SQL DDL 或 Mongo `createIndex`/`dropIndex`）。

按执行确认模式进入下一步：
- `需确认模式`：只有用户明确确认后，才能进入下一步执行。
- `免确认模式`：无需等待用户确认，直接进入下一步执行；但必须在输出中记录“免确认执行”。

#### 删除旧索引的专属门槛（必须全部满足）
1. 旧索引不合理证据：
   - explain 显示长期不命中，或命中后扫描量/代价明显劣于候选索引；
   - 与其他索引存在前缀/覆盖重叠，且业务查询已可被替代索引覆盖。
2. 替代索引保障：
   - 必须先明确“由哪个现有/新建索引替代”；
   - 对核心查询执行替代前后 explain，对比不退化（命中、扫描行数、关键计划节点）。
3. 删除安全性：
   - 给出删除后潜在影响与回滚路径（重建索引语句）；
   - 未完成替代验证时，只能标记“候选删除”，不得执行 `DROP INDEX`/`dropIndex`。

### 5) 执行索引变更并运行 explain

1. SQL 数据库：在 `docs/sql/<date>_<table>_index_optimization.sql` 中写 DDL。
2. MongoDB：输出 `createIndex` 与对应 `dropIndex` 回滚语句。
3. 对每条代表查询（单查询模式下即目标查询），在索引变更前后都执行 explain。
4. 记录输出并标注是否命中目标索引，且必须写明实际命中的索引名（未命中时标注 `NONE` 或等效状态）。
5. 涉及删除旧索引时，必须先验证替代索引命中，再执行删除语句。

### 6) 迭代到命中或达到停止条件

如果 explain 未命中预期索引：
1. 诊断原因：前导列错误、选择性过低、排序不匹配、隐式转换、统计信息过旧、优化器选择偏差等。
2. 调整索引设计（重排序、增减后缀列、拆分过宽索引、删除冗余索引）。
3. 重新运行 explain。
4. 重复执行，直到命中目标索引或达到 3 次重设计上限。

若 3 次重设计后仍未命中，停止并报告根因与最稳妥替代方案。

## 输出内容

按以下顺序输出：
1. `表与数据库上下文`
2. `查询输入`
   - 全量模式：查询清单（含可点击代码位置）
   - 单查询模式：目标查询 + 可选可点击代码位置 + 当前已有索引
3. `访问模式汇总`
4. `索引方案（DDL + 使用位置）`
5. `索引变更依据与确认记录`
   - 需确认模式：记录用户确认内容
   - 免确认模式：记录“免确认执行”声明
6. `Explain 验证（优化前/后）`
   - 每条查询都要包含：是否命中、命中索引名（或 `NONE`）、关键计划信息（如 `type/rows/Extra` 或执行计划节点）
7. `迭代日志`
8. `最终建议`
9. `回滚 SQL`

## 质量规则

- 索引优化前必须先拿到表名或集合名。
- 必须提供可跳转代码位置，且使用 Markdown 绝对路径链接格式：`[path:line](/absolute/path/to/file#Lline)`。
- 全量模式必须“汇总全部查询”后再定最终索引。
- 单查询模式不得扩展分析其他查询，必须先查询数据库已有索引。
- 创建/删除索引前，必须先给出依据与待执行语句。
- `需确认模式` 下，未获确认不得执行索引创建或删除。
- `免确认模式` 下，可直接执行索引创建或删除，但必须记录“免确认执行”。
- 删除旧索引建议必须同时提供“不合理证据 + 替代索引 + explain 不退化验证”。
- 每个新增索引都必须附回滚语句（SQL `DROP INDEX` 或 Mongo `dropIndex`）。
- Explain 结果必须明确“命中索引名”；仅写“已命中/未命中”不合格。
- 没有 explain 证据，不得宣称“已优化”。

## 参考资源

- 数据库索引与 EXPLAIN 规则：`references/index-rules.md`
- 查询定位脚本：`scripts/collect_table_queries.py`

## 快速命令

```bash
# 1) 查询定位（含 path:line）
python3 $CODEX_HOME/skills/index-optimization-skill/scripts/collect_table_queries.py --table wallet --repo-root .

# 2) 手工补充扫描
rg -n --no-heading -S "wallet|FROM|JOIN|UPDATE|INSERT INTO|DELETE FROM|Collection\\(|\\.find\\(|\\.aggregate\\(" apps pkg docs

# 3) 单查询模式先查已有索引（示例）
mysql -e "SHOW INDEX FROM wallet;"
psql -c "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'wallet';"
mongosh --eval "db.wallet.getIndexes()"

# 4) 验证 Skill 结构
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/index-optimization-skill
```
