# KingbaseES 核心SQL参考 — 测试用例

独立测试用例，验证 AI 无需查阅外部文档即可给出正确回答。

## 测试用例格式

| 字段 | 说明 |
|------|------|
| 编号 | TC-CORE_NNN |
| 场景 | 真实使用场景描述 |
| 输入问题 | 用户向AI提出的问题 |
| 期望答案要点 | AI回答必须包含的关键点 |
| 验证方法 | 如何判断AI回答正确 |

---

## 1. DDL/DML 基础 (4个测试用例)

### TC-CORE-001: 创建分区表

**场景**：需要在KingbaseES中创建按日期范围分区的销售表。

**输入问题**：KingbaseES如何创建按年份分区的 RANGE 分区表？

**期望答案要点**：
- 使用 `PARTITION BY RANGE` 语法
- 主表声明：`CREATE TABLE sales (...) PARTITION BY RANGE (sold_at)`
- 分区子表：`CREATE TABLE sales_y2024 PARTITION OF sales FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')`
- 分区列必须包含在分区键中
- 支持 LIST 和 HASH 分区类型

**验证方法**：AI输出包含PARTITION BY RANGE语法和FOR VALUES FROM...TO分区定义。

---

### TC-CORE-002: UPSERT操作

**场景**：数据同步场景，存在则更新，不存在则写入。

**输入问题**：KingbaseES如何实现UPSERT（冲突更新）？

**期望答案要点**：
- 使用 `INSERT ... ON CONFLICT` 语法
- `ON CONFLICT (column) DO UPDATE SET col = EXCLUDED.col`
- `EXCLUDED` 关键字引用冲突行的拟写入值
- 可加WHERE条件：`ON CONFLICT (id) DO UPDATE SET ... WHERE OLD.condition`
- 也可 `DO NOTHING` 忽略冲突

**验证方法**：AI给出了ON CONFLICT完整语法，包含EXCLUDED关键字引用。

---

### TC-CORE-003: 序列操作

**场景**：需要创建和使用自增序列。

**输入问题**：KingbaseES中如何创建序列并在写入数据时使用？

**期望答案要点**：
- 创建序列：`CREATE TABLE t (id SERIAL PRIMARY KEY, ...)` 或 `CREATE SEQ seqname START 1 INCREMENT 1`
- 取值：`nextval('seq_name')`
- 查看当前值：`currval('seq_name')`
- 重置：`setval('seq_name', value)`
- SERIAL自动创建序列名格式：`table_col_seq`

**验证方法**：AI说明了SERIAL自动创建序列和nextval/currval的使用方式。

---

### TC-CORE-004: 索引策略

**场景**：查询性能差，需要创建合适的索引。

**输入问题**：KingbaseES支持哪些类型的索引？如何创建部分索引和表达式索引？

**期望答案要点**：
- 普通B-tree索引：`CREATE INDEX idx ON t(col)`
- 唯一索引：`CREATE UNIQUE INDEX idx ON t(col)`
- 部分索引：`CREATE INDEX idx ON t(col) WHERE condition`
- 表达式索引：`CREATE INDEX idx ON t((expression))`
- 复合索引：`CREATE INDEX idx ON t(col1, col2)`
- 索引类型选项：B-tree, Hash, GiST, GIN, SP-GiST, BRIN
- GIN用于JSONB/数组，BRIN用于超大表

**验证方法**：AI列出了至少普通、唯一、部分、表达式四种索引类型及创建语法。

---

## 2. PL/SQL 编程 (4个测试用例)

### TC-CORE-005: 存储过程

**场景**：需要编写一个存储过程完成批量数据处理。

**输入问题**：KingbaseES如何编写带游标的存储过程？

**期望答案要点**：
- 使用 `CREATE OR REPLACE PROCEDURE` 语法
- 游标声明：`CURSOR cur IS SELECT ...`
- 游标遍历：`FOR rec IN cur LOOP ... END LOOP`
- 动态游标：`OPEN cur FOR dynamic_sql`
- 参数模式：IN, OUT, IN OUT
- 使用 `CALL proc_name(args)` 调用

**验证方法**：AI给出了CREATE PROCEDURE语法和游标遍历的FOR循环写法。

---

### TC-CORE-006: 函数编写

**场景**：需要创建一个可复用的计算函数。

**输入问题**：KingbaseES如何创建返回表的函数？

**期望答案要点**：
- 使用 `CREATE OR REPLACE FUNCTION` 语法
- 返回集合：`RETURNS SETOF record_type` 或 `RETURNS TABLE(col type, ...)`
- 使用 `RETURN QUERY SELECT ...` 返回多行
- 或使用 `RETURN NEXT value` 逐行返回
- 语言指定：`LANGUAGE plsql` 或 `LANGUAGE sql`
- 函数调用：`SELECT * FROM func_name(args)`

**验证方法**：AI说明了RETURNS TABLE/SETOF和RETURN QUERY的使用方式。

---

### TC-CORE-007: 触发器

**场景**：需要在数据变更时自动记录审计日志。

**输入问题**：如何在KingbaseES创建INSERT触发器来记录操作日志？

**期望答案要点**：
- 创建触发器函数：`CREATE FUNCTION log_func() RETURNS TRIGGER AS $$ ... $$`
- 访问新旧值：`NEW.column` / `OLD.column`
- 触发器属性：`TG_OP` 判断操作类型
- 创建触发器：`CREATE TRIGGER trg_name BEFORE/AFTER INSERT ON table FOR EACH ROW EXECUTE FUNCTION log_func()`
- 返回：返回NEW(BEFORE)或NULL(阻止操作)
- 支持 `WHEN (condition)` 条件触发
- 支持 `FOR EACH STATEMENT` 语句级触发器

**验证方法**：AI给出了触发器函数和CREATE TRIGGER的完整语法。

---

### TC-CORE-008: 异常处理

**场景**：存储过程中需要捕获和处理错误。

**输入问题**：KingbaseES PL/SQL中如何处理异常？

**期望答案要点**：
- 使用 `EXCEPTION` 块
- 格式：`BEGIN ... EXCEPTION WHEN condition THEN ... WHEN OTHERS THEN ... END`
- 常见异常：`NO_DATA_FOUND`, `TOO_MANY_ROWS`, `ZERO_DIVISION`, `DUPLICATE_VALUE`
- 获取错误信息：`SQLCODE`, `SQLERRM`, `ERA_CODE`, `ERA_MESSAGE`
- 使用 `GET STACKED DIAGNOSTICS` 获取详细错误
- 可嵌套BEGIN块实现精细化异常处理

**验证方法**：AI给出了EXCEPTION块的语法和常用异常类型。

---

## 3. Oracle 兼容性 (4个测试用例)

### TC-CORE-009: 兼容模式切换

**场景**：从Oracle迁移，需要启用兼容模式。

**输入问题**：如何启用和验证KingbaseES的Oracle兼容模式？

**期望答案要点**：
- 查看：`SHOW oracle_compatible`
- 会话级：`SET oracle_compatible = on`
- 永久启用：`ALTER SYSTEM SET oracle_compatible = on` 然后 `SELECT sys_reload_conf()`
- 部分参数需要重启
- 兼容模式下双引号标识符转大写
- 兼容模式影响：空字符串当NULL处理、自连接运算符、NVL/DECODE可用

**验证方法**：AI给出了SHOW/SET/ALTER SYSTEM三层配置方式和sys_reload_conf()重载方法。

---

### TC-CORE-010: 函数映射

**场景**：Oracle SQL中使用NVL和DECODE函数，需要找到KingbaseES等价写法。

**输入问题**：Oracle的NVL和DECODE函数在KingbaseES中怎么等价实现？

**期望答案要点**：
- NVL(col, default) → COALESCE(col, default)
- Oracle兼容模式下NVL可直接使用
- DECODE(x, a, b, c) → CASE WHEN x=a THEN b ELSE c END
- Oracle兼容模式下DECODE可直接使用
- 层级查询：START WITH...CONNECT BY → WITH RECURSIVE
- 序列：seq.NEXTVAL → nextval('seq')

**验证方法**：AI给出了NVL→COALESCE和DECODE→CASE的映射关系。

---

### TC-CORE-011: 数据类型映射

**场景**：Oracle表结构迁移到KingbaseES。

**输入问题**：Oracle的VARCHAR2和NUMBER类型在KingbaseES中等价于什么？

**期望答案要点**：
- VARCHAR2(n) → VARCHAR(n)（兼容模式下可直接用VARCHAR2）
- NUMBER(p,s) → NUMERIC(p,s)（兼容模式下可直接用NUMBER）
- NUMBER 无精度 → BIGINT
- NUMBER(1) → BOOLEAN（部分场景）
- CLOB → CLOB，BLOB → BYTEA
- RAW(n) → BYTEA(n)
- DATE类型在KES中不含时间部分，含时间用TIMESTAMP
- Oracle兼容模式下数据类型自动识别

**验证方法**：AI正确列出了VARCHAR2→VARCHAR和NUMBER→NUMERIC的映射。

---

### TC-CORE-012: 分页差异

**场景**：Oracle分页查询迁移到KingbaseES。

**输入问题**：Oracle的ROWNUM分页在KingbaseES中如何改写？

**期望答案要点**：
- Oracle `WHERE ROWNUM <= N` → KES `LIMIT N`
- Oracle分页：`SELECT * FROM (SELECT *, ROWNUM rn FROM t WHERE ROWNUM <= end) WHERE rn > start`
- KES分页：`SELECT * FROM t ORDER BY id LIMIT pageSize OFFSET offset`
- 键集分页：`WHERE id > last_id ORDER BY id LIMIT pageSize`
- Oracle兼容模式下仍推荐用LIMIT

**验证方法**：AI给出了ROWNUM→LIMIT/OFFSET的转换方法。

---

## 4. 系统目录查询 (3个测试用例)

### TC-CORE-013: 查看表结构

**场景**：需要查看某张表的完整结构信息。

**输入问题**：如何查看KingbaseES中某张表的列名、类型和约束？

**期望答案要点**：
- 查询 `sys_information_schema.columns`
- `SELECT column_name, data_type, is_nullable, column_default, character_maximum_length FROM sys_information_schema.columns WHERE table_name = 't'`
- 或查 `sys_class` join `sys_attribute`
- 查看约束：查 `sys_information_schema.table_constraints`
- `\d table_name` 在ksql客户端

**验证方法**：AI给出了sys_information_schema.columns查询方法和ksql的\d命令。

---

### TC-CORE-014: 查看索引

**场景**：需要分析表的索引使用情况。

**输入问题**：如何查看KingbaseES表的索引定义和使用统计？

**期望答案要点**：
- 查看索引定义：`SELECT indexname, indexdef FROM sys_indexes WHERE tablename = 't'`
- 或使用ksql：`\di table_name`
- 查看使用统计：`SELECT indexrelname, idx_scan, idx_tup_read FROM sys_stat_user_indexes WHERE relname = 't'`
- idx_scan为0表示索引未被使用
- 查看表大小：`SELECT sys_size_pretty(sys_relation_size('t'))`

**验证方法**：AI给出了sys_indexes和sys_stat_user_indexes的查询方法。

---

### TC-CORE-015: 权限查看

**场景**：需要审计某用户的数据库权限。

**输入问题**：如何查看KingbaseES中某个用户的所有权限？

**期望答案要点**：
- 查表权限：`SELECT grantee, table_name, privilege_type FROM sys_table_privileges WHERE grantee = 'user'`
- 查角色成员：查 `sys_auth_members` join `sys_authid`
- 查Schema权限：查 `sys_schema_privileges`
- 查默认权限：查 `sys_default_acl`
- 用户属性：`SELECT * FROM sys_user WHERE usename = 'user'`

**验证方法**：AI给出了sys_table_privileges和sys_auth_members的查询路径。

---

## 5. 高级查询 (3个测试用例)

### TC-CORE-016: 窗口函数

**场景**：需要按部门排名员工薪资。

**输入问题**：KingbaseES如何使用窗口函数实现分组排名？

**期望答案要点**：
- `RANK() OVER (PARTITION BY dept ORDER BY salary DESC)` — 跳跃排名
- `DENSE_RANK() OVER (...)` — 连续排名
- `ROW_NUMBER() OVER (...)` — 行号
- `LEAD()/LAG()` — 前后行访问
- `AVG() OVER (PARTITION BY dept)` — 窗口聚合
- `NTILE(n)` — 分桶
- `FIRST_VALUE()/LAST_VALUE()` — 首尾值

**验证方法**：AI给出了RANK/DENSE_RANK/ROW_NUMBER的区别和OVER语法。

---

### TC-CORE-017: 递归CTE

**场景**：查询组织层级结构。

**输入问题**：KingbaseES如何实现递归查询，比如查询部门层级树？

**期望答案要点**：
- 使用 `WITH RECURSIVE` 语法
- 锚点（基准）：`SELECT id, parent_id, 1 AS depth FROM t WHERE parent_id IS NULL`
- 递归部分：`UNION ALL SELECT t.id, t.parent_id, r.depth+1 FROM t JOIN cte r ON t.parent_id = r.id`
- 防止无限循环：加深度限制 `WHERE r.depth < 10`
- 替代Oracle的 `START WITH ... CONNECT BY`

**验证方法**：AI给出了WITH RECURSIVE的完整语法结构（锚点+递归部分+UNION ALL）。

---

### TC-CORE-018: JSON操作

**场景**：需要查询和更新JSONB字段。

**输入问题**：KingbaseES如何查询和索引JSONB数据？

**期望答案要点**：
- 取值操作符：`->` (返回JSON), `->>` (返回文本)
- 路径访问：`data->'key'->'subkey'`
- 包含检查：`@>` 操作符，如 `data @> '{"color":"red"}'`
- 存在检查：`?` 操作符，如 `data ? 'key'`
- GIN索引：`CREATE INDEX idx ON t USING GIN(jsonb_col)`
- 更新：`jsonb_set(data, '{key}', '"value"')`
- 删除键：`data - 'key'`

**验证方法**：AI给出了`->>`和`->`的区别以及GIN索引创建方法。

---

## 6. 事务与锁 (2个测试用例)

### TC-CORE-019: 事务保存点

**场景**：批量操作中部分失败需要回滚到特定点。

**输入问题**：KingbaseES如何使用保存点实现部分回滚？

**期望答案要点**：
- 开启事务：`BEGIN`
- 创建保存点：`SAVEPOINT sp1`
- 回滚到保存点：`ROLLBACK TO sp1`
- 释放保存点：`RELEASE sp1`
- 保存点可嵌套
- 回滚到保存点后事务仍有效，可继续执行
- `COMMIT` 或 `ROLLBACK` 结束事务并清除所有保存点

**验证方法**：AI给出了SAVEPOINT和ROLLBACK TO的完整使用流程。

---

### TC-CORE-020: 锁排查

**场景**：生产环境出现锁等待，需要排查。

**输入问题**：如何查看KingbaseES中的锁等待情况并解决阻塞？

**期望答案要点**：
- 查询未授予的锁：`SELECT * FROM sys_locks WHERE NOT granted`
- 关联 `sys_stat_activity` 获取PID和用户信息
- 通过 `relation` 字段匹配阻塞关系
- 终止阻塞源：`SELECT sys_terminate_pid(blocking_pid)`
- 取消查询：`SELECT sys_cancel_pid(pid)`
- 设置超时：`SET lock_timeout = '10s'`
- 预防：避免长事务、使用合适的隔离级别

**验证方法**：AI给出了sys_locks WHERE NOT granted和sys_terminate_pid的用法。

---

## 7. 错误诊断 (2个测试用例)

### TC-CORE-021: 错误代码解读

**场景**：执行SQL时报错，需要根据错误代码定位问题。

**输入问题**：KingbaseES报错 23505 是什么意思？

**期望答案要点**：
- SQLSTATE 23505 = unique_violation（唯一性约束违例）
- 表示写入或更新的数据违反了唯一约束
- 检查表上的UNIQUE约束或主键
- 解决：检查重复数据或使用ON CONFLICT处理
- 23开头 = integrity constraint violation 类别

**验证方法**：AI正确识别23505为唯一性约束违例。

---

### TC-CORE-022: 标识符大小写

**场景**：Oracle迁移后查询报错找不到表。

**输入问题**：KingbaseES中标识符大小写敏感吗？双引号有什么影响？

**期望答案要点**：
- 标准模式：无引号标识符自动转小写
- Oracle兼容模式：无引号标识符自动转大写
- 双引号内的标识符保持原始大小写
- `"MyTable"` ≠ `mytable`（标准模式）
- 建议在KES中统一使用小写、无引号命名
- Oracle迁移时注意：Oracle对象名默认大写，需在兼容模式下访问

**验证方法**：AI说明了双引号保持大小写和无引号自动转换的规则。

---

## 测试覆盖率统计

| 领域 | 测试用例数 | 覆盖范围 |
|------|-----------|---------|
| DDL/DML 基础 | 4 | 分区表, UPSERT, 序列, 索引 |
| PL/SQL 编程 | 4 | 存储过程, 函数, 触发器, 异常处理 |
| Oracle 兼容性 | 4 | 模式切换, 函数映射, 类型映射, 分页 |
| 系统目录查询 | 3 | 表结构, 索引统计, 权限审计 |
| 高级查询 | 3 | 窗口函数, 递归CTE, JSON操作 |
| 事务与锁 | 2 | 保存点, 锁排查 |
| 错误诊断 | 2 | 错误代码, 标识符大小写 |
| **合计** | **22** | 覆盖7大领域 |
