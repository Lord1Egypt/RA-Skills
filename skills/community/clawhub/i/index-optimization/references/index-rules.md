# 各数据库索引规则

用于设计可复用索引与评估 EXPLAIN 结果。

## MySQL 8 / InnoDB

### 复合索引列顺序
- 等值条件列优先。
- 范围条件列其次。
- 排序列（`ORDER BY`）尽量放后面。
- 出现首个范围条件后，不再期待后续列被完整利用。

### 可复用性规则
- 优先用一个共享复合索引覆盖多个高频查询。
- 避免大量左前缀重叠索引。
- 每加一个索引都要评估写入开销。

### EXPLAIN 命中目标
- `key` 为预期索引名。
- `type` 理想为 `const` / `ref` / `range`（大表尽量避免 `ALL`）。
- `rows` 相比基线显著下降。
- `Extra` 尽量避免明显 `Using filesort` 或 `Using temporary`。

### 常见未命中原因
- 前导列不匹配。
- 条件里对索引列做函数或隐式转换。
- 前导列选择性过低。
- 排序与索引后缀不匹配。
- 统计信息过旧。

## TiDB

### 核心要点
- 遵循 MySQL 兼容的索引顺序规则。
- 用 `EXPLAIN ANALYZE` 观察优化器选择。
- 检查下推谓词是否真的走了索引范围扫描。
- 大扫描场景下确认 cop/root task 计划形态。

### 常见未命中模式
- 统计信息或 pseudo stats 导致次优计划。
- 谓词改写阻断索引范围下推。
- 计划缓存采用通用计划，不适配参数倾斜。

## PostgreSQL

### 复合索引列顺序
- 等值在前，范围在后，排序列再后。
- 不同前导条件可考虑拆分独立索引。
- 稳定过滤条件可用部分索引（如 `is_del = false`）。

### EXPLAIN 命中目标
- 预期场景下应看到 `Index Scan` 或 `Bitmap Index Scan`。
- 在 `EXPLAIN ANALYZE` 对比 `actual rows` 与 `estimated rows`。
- 大表应命中索引时，重点关注是否退化为 `Seq Scan`。

### 常见未命中原因
- 类型不匹配阻断索引（`::text`、隐式转换）。
- 统计信息过旧导致 planner 倾向顺序扫描。
- 查询条件与部分索引谓词不匹配。

## MongoDB

### 复合索引顺序（ESR）
- Equality（等值）字段优先。
- Sort（排序）字段其次。
- Range（范围）字段最后。
- 尽量让高频查询共享同一前缀，减少重叠索引。

### 索引设计要点
- 常见语句：`db.collection.createIndex({a:1,b:-1})`。
- 稳定过滤条件可考虑 `partialFilterExpression`。
- 数组字段会触发 multikey 索引，组合设计前先确认查询形态。
- 避免无上限堆叠索引，关注写入放大与内存占用。

### explain 命中目标
- 使用 `explain("executionStats")`。
- `winningPlan` 中应出现 `IXSCAN`（必要时伴随 `FETCH`）。
- `COLLSCAN` 在大集合高频路径应尽量消除。
- 关注 `totalKeysExamined`、`totalDocsExamined` 是否显著下降。

### 常见未命中原因
- 查询谓词与索引前缀不匹配。
- 排序方向与索引定义不一致。
- 使用 `$expr` / 函数计算导致难以走索引。
- 低选择性字段放在复合索引前缀。

## 跨数据库检查清单

1. 索引设计前先确认全部查询分组。
2. 选择最小可复用索引集合。
3. 每条代表查询都要做 EXPLAIN 验证。
4. 每个新增索引都保留回滚语句（SQL `DROP INDEX` / Mongo `dropIndex`）。
5. 迭代到命中目标计划，或 3 次重设计后停止。
