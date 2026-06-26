---
name: pg-execute
description: |
  PostgreSQL 安全 SQL 执行工具。支持只读模式和访问控制，安全地执行 SQL 查询和命令。
  当用户需要执行 SQL、查询数据、更新数据、插入数据、删除数据时使用。
---

## 功能说明

pg-execute 提供安全的 SQL 执行能力，支持只读模式和多层安全控制。

## 执行流程

### 1. 前置检查

确认 postgres-mcp MCP 工具可用（参考根 SKILL.md 的前置检查）。

### 2. 检查执行模式

确认 postgres-mcp 的运行模式：

- **只读模式（Restricted）** — 只允许 SELECT 查询
- **完全模式（Unrestricted）** — 允许所有 SQL 操作

可以通过配置或环境变量确定当前模式。

### 3. SQL 分类和验证

根据 SQL 类型进行不同的处理：

#### 读操作（SELECT）

**特点**：
- 不修改数据
- 只读模式和完全模式都允许
- 相对安全

**验证**：
- 检查查询是否合法
- 避免过于复杂的查询（防止资源耗尽）
- 考虑添加 LIMIT（如果没有）

**示例**：
```sql
SELECT * FROM orders WHERE user_id = 123;
SELECT COUNT(*) FROM users;
SELECT u.name, o.total_amount 
FROM users u 
JOIN orders o ON u.id = o.user_id;
```

#### 写操作（INSERT、UPDATE、DELETE）

**特点**：
- 修改数据
- 只在完全模式下允许
- 需要用户确认

**验证**：
- 检查是否在只读模式（拒绝执行）
- 检查是否有 WHERE 条件（避免误操作）
- 向用户展示将要执行的 SQL 并确认

**示例**：
```sql
INSERT INTO orders (user_id, status, total_amount) 
VALUES (123, 'pending', 99.99);

UPDATE orders 
SET status = 'paid' 
WHERE id = 456;

DELETE FROM orders 
WHERE id = 789 AND status = 'cancelled';
```

#### DDL 操作（CREATE、ALTER、DROP）

**特点**：
- 修改数据库结构
- 只在完全模式下允许
- 需要特别谨慎

**验证**：
- 检查是否在只读模式（拒绝执行）
- 强制要求用户确认
- 建议在事务中执行（可回滚）
- 生产环境建议手动执行

**示例**：
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);

ALTER TABLE orders ADD COLUMN notes TEXT;

DROP INDEX idx_old_index;
```

### 4. 安全检查

在执行前进行多层安全检查：

#### SQL 注入防护

使用参数化查询：

```python
# ❌ 不安全
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 安全
query = "SELECT * FROM users WHERE id = %s"
params = (user_id,)
```

#### 危险操作检测

检测并警告危险操作：

```sql
-- ⚠️ 危险：无条件删除
DELETE FROM orders;

-- ⚠️ 危险：删除整个表
DROP TABLE orders;

-- ⚠️ 危险：无条件更新
UPDATE orders SET status = 'cancelled';
```

#### 资源限制

- **查询超时** — 设置 statement_timeout 防止长时间运行
- **结果集限制** — 自动添加 LIMIT 防止返回过多数据
- **并发控制** — 限制同时执行的查询数量

### 5. 执行 SQL

根据不同类型的 SQL 采用不同的执行策略：

#### SELECT 查询

直接执行并返回结果：

```python
result = execute_query("SELECT * FROM orders WHERE user_id = %s", (123,))
```

返回格式：
```json
{
  "columns": ["id", "user_id", "status", "total_amount", "created_at"],
  "rows": [
    [1, 123, "pending", 99.99, "2024-01-01 10:00:00"],
    [2, 123, "paid", 149.99, "2024-01-02 11:00:00"]
  ],
  "row_count": 2,
  "execution_time": 0.05
}
```

#### 写操作

在事务中执行，支持回滚：

```python
try:
    begin_transaction()
    result = execute_query("UPDATE orders SET status = %s WHERE id = %s", ("paid", 456))
    commit_transaction()
except Exception as e:
    rollback_transaction()
    raise e
```

#### DDL 操作

建议使用 CONCURRENTLY 避免锁表：

```sql
-- 创建索引（不锁表）
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);

-- 删除索引（不锁表）
DROP INDEX CONCURRENTLY idx_old_index;
```

### 6. 结果展示

将执行结果以易读的格式展示给用户：

#### 查询结果

```
📊 查询结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

查询：SELECT * FROM orders WHERE user_id = 123

结果：2 行

| id  | user_id | status  | total_amount | created_at          |
|-----|---------|---------|--------------|---------------------|
| 1   | 123     | pending | 99.99        | 2024-01-01 10:00:00 |
| 2   | 123     | paid    | 149.99       | 2024-01-02 11:00:00 |

执行时间：0.05 秒
```

#### 写操作结果

```
✅ 执行成功
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SQL：UPDATE orders SET status = 'paid' WHERE id = 456

影响行数：1 行
执行时间：0.02 秒
```

#### 错误信息

```
❌ 执行失败
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SQL：SELECT * FROM non_existent_table

错误：relation "non_existent_table" does not exist

建议：检查表名是否正确，或使用 /pg-schema 查看可用的表
```

### 7. 事务管理

支持显式事务控制：

```
用户：开始一个事务

助手：BEGIN;
     事务已开始，后续操作将在事务中执行
     
用户：更新订单状态
     UPDATE orders SET status = 'paid' WHERE id = 456

助手：[执行更新]
     影响 1 行
     
用户：提交事务

助手：COMMIT;
     事务已提交，更改已保存
```

回滚示例：

```
用户：开始事务
助手：BEGIN;

用户：删除订单
     DELETE FROM orders WHERE id = 456
     
助手：[执行删除]
     影响 1 行
     
用户：等等，我不想删除，回滚

助手：ROLLBACK;
     事务已回滚，更改已撤销
```

## 使用示例

**简单查询**：
```
用户：查询用户 123 的订单

助手：SELECT * FROM orders WHERE user_id = 123;
     [执行并展示结果]
```

**带确认的写操作**：
```
用户：把订单 456 的状态改为 paid

助手：将执行以下 SQL：
     UPDATE orders SET status = 'paid' WHERE id = 456
     
     这将修改 1 行数据，是否确认？
     
用户：确认

助手：[执行更新]
     ✅ 更新成功，影响 1 行
```

**只读模式拒绝**：
```
用户：删除订单 789

助手：❌ 当前运行在只读模式，不允许执行写操作
     
     如果需要执行写操作，请：
     1. 重新配置 postgres-mcp 为完全模式
     2. 或在有写权限的环境中执行
```

**批量操作**：
```
用户：批量更新这些订单的状态

助手：BEGIN;
     UPDATE orders SET status = 'shipped' WHERE id IN (1, 2, 3);
     COMMIT;
     
     ✅ 更新成功，影响 3 行
```

## 安全最佳实践

### 1. 使用参数化查询

```python
# ❌ 不安全
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ 安全
query = "SELECT * FROM users WHERE email = %s"
execute_query(query, (email,))
```

### 2. 最小权限原则

- 只读场景使用只读账户
- 生产环境避免使用超级用户
- 按需授予权限

### 3. 审计日志

记录所有执行的 SQL：

```
[2024-01-01 10:00:00] user=alice query="SELECT * FROM orders" rows=100 time=0.05s
[2024-01-01 10:01:00] user=bob query="UPDATE orders SET status='paid' WHERE id=456" rows=1 time=0.02s
```

### 4. 备份和恢复

写操作前建议：
- 确认有最新备份
- 在测试环境先验证
- 使用事务（可回滚）

### 5. 生产环境保护

- 启用只读模式
- 设置查询超时
- 限制结果集大小
- 禁止危险操作（DROP、TRUNCATE）

## 配置选项

### 只读模式

```bash
# 启动时指定
postgres-mcp --read-only "postgresql://..."

# 环境变量
export POSTGRES_MCP_READ_ONLY=true
```

### 查询超时

```bash
# 设置 30 秒超时
postgres-mcp --query-timeout 30 "postgresql://..."

# 或在 SQL 中设置
SET statement_timeout = '30s';
```

### 结果集限制

```bash
# 最多返回 1000 行
postgres-mcp --max-rows 1000 "postgresql://..."
```

## 注意事项

1. **只读模式** — 生产环境建议使用只读模式，避免误操作
2. **确认机制** — 写操作前必须向用户确认
3. **事务使用** — 重要操作在事务中执行，出错可回滚
4. **权限检查** — 确保数据库用户有足够权限
5. **性能影响** — 大量数据操作可能影响数据库性能，选择合适时机
6. **备份优先** — 重要操作前确保有备份

## 相关命令

```sql
-- 查看当前事务状态
SELECT * FROM pg_stat_activity WHERE pid = pg_backend_pid();

-- 查看锁信息
SELECT * FROM pg_locks;

-- 查看长时间运行的查询
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '1 minute';

-- 终止查询
SELECT pg_cancel_backend(pid);  -- 温和终止
SELECT pg_terminate_backend(pid);  -- 强制终止
```
