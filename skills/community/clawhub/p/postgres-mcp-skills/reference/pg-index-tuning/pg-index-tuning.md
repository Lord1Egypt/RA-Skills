---
name: pg-index-tuning
description: |
  PostgreSQL 索引优化工具。使用工业级算法探索数千种可能的索引组合，为工作负载找到最佳索引方案。
  当用户提到慢查询、索引优化、性能调优、查询太慢、需要加索引时使用。
---

## 功能说明

pg-index-tuning 使用先进的索引优化算法，分析查询工作负载，推荐最优的索引方案。

## 执行流程

### 1. 前置检查

确认 postgres-mcp MCP 工具可用（参考根 SKILL.md 的前置检查）。

### 2. 收集工作负载

有两种方式收集需要优化的查询：

#### 方式一：用户提供具体查询

用户直接提供需要优化的 SQL 查询。

```
用户：这个查询太慢了，帮我优化一下
     SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'
```

#### 方式二：分析慢查询日志

如果数据库启用了慢查询日志，可以从 `pg_stat_statements` 视图获取最慢的查询。

```sql
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 3. 调用索引优化工具

使用 `suggest_indexes` 或类似的 MCP 工具分析查询并推荐索引。

传入参数：
- **查询列表** — 需要优化的 SQL 查询
- **工作负载权重** — 每个查询的执行频率（可选）
- **约束条件** — 最大索引数量、最大索引大小等（可选）

### 4. 分析推荐结果

索引优化工具会返回：

#### 推荐的索引
- **索引定义** — CREATE INDEX 语句
- **预期收益** — 查询性能提升百分比
- **索引大小** — 预估的磁盘空间占用
- **影响的查询** — 哪些查询会使用这个索引

#### 优化前后对比
- **当前性能** — 优化前的查询执行时间
- **优化后性能** — 添加索引后的预期执行时间
- **性能提升** — 提升的百分比

#### 成本分析
- **空间成本** — 所有推荐索引的总大小
- **维护成本** — 索引对写操作的影响
- **收益** — 查询性能的总体提升

### 5. 生成优化方案

将推荐结果整理成清晰的优化方案：

```
🎯 索引优化方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 当前问题：
  • 查询 A：平均 2.5s，全表扫描 orders 表
  • 查询 B：平均 1.8s，全表扫描 users 表

💡 推荐索引：

1. CREATE INDEX idx_orders_user_status 
   ON orders(user_id, status);
   
   收益：查询 A 提速 95% (2.5s → 0.12s)
   成本：约 150MB 磁盘空间

2. CREATE INDEX idx_users_email 
   ON users(email);
   
   收益：查询 B 提速 90% (1.8s → 0.18s)
   成本：约 80MB 磁盘空间

📈 总体效果：
  • 查询性能提升：92%
  • 磁盘空间占用：230MB
  • 写操作影响：约 5% 性能下降
```

### 6. 执行确认

在实际创建索引前，询问用户确认：

1. **展示完整的 CREATE INDEX 语句**
2. **说明预期收益和成本**
3. **提醒索引创建可能需要较长时间**（大表）
4. **建议在低峰期执行**（生产环境）

用户确认后，可以：
- 直接执行 CREATE INDEX（如果有权限）
- 生成 SQL 脚本供用户手动执行
- 使用 `CONCURRENTLY` 选项避免锁表（PostgreSQL 11+）

### 7. 验证效果

索引创建后，验证优化效果：

1. **重新执行查询** — 对比优化前后的执行时间
2. **检查索引使用** — 确认查询确实使用了新索引
3. **监控性能** — 观察一段时间，确保没有副作用

## 高级功能

### 假设索引（Hypothetical Indexes）

在不实际创建索引的情况下，模拟索引对查询计划的影响：

```sql
-- 创建假设索引
SELECT * FROM hypopg_create_index('CREATE INDEX ON orders(user_id)');

-- 查看查询计划
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- 清理假设索引
SELECT hypopg_reset();
```

### 多查询优化

同时优化多个查询，找到最优的索引组合：

```
用户：优化这些查询
     查询1：SELECT * FROM orders WHERE user_id = ?
     查询2：SELECT * FROM orders WHERE status = ?
     查询3：SELECT * FROM orders WHERE user_id = ? AND status = ?

助手：分析发现，创建一个复合索引 (user_id, status) 
     可以同时优化所有三个查询
```

### 索引维护建议

除了添加新索引，还可以：

- **删除未使用的索引** — 释放空间，减少写操作开销
- **重建膨胀的索引** — REINDEX 恢复性能
- **合并重复索引** — 删除功能重复的索引

## 使用示例

**单个查询优化**：
```
用户：这个查询太慢了
     SELECT * FROM orders WHERE user_id = 123 AND created_at > '2024-01-01'
     
助手：[分析查询]
     建议创建索引：
     CREATE INDEX idx_orders_user_created 
     ON orders(user_id, created_at);
     
     预期提速 90%，是否创建？
```

**工作负载优化**：
```
用户：分析最近一周的慢查询，给出优化建议

助手：[从 pg_stat_statements 获取慢查询]
     [调用索引优化工具]
     [生成综合优化方案]
```

## 注意事项

1. **索引不是万能的** — 过多索引会影响写性能，需要权衡
2. **复合索引顺序** — 索引列的顺序很重要，遵循"选择性高的列在前"原则
3. **部分索引** — 对于有明显过滤条件的查询，考虑使用部分索引节省空间
4. **表达式索引** — 对于函数调用（如 LOWER(email)），考虑表达式索引
5. **CONCURRENTLY** — 生产环境创建索引时使用 CONCURRENTLY 避免锁表
6. **监控效果** — 索引创建后持续监控，确保达到预期效果

## 相关工具

- **pg_stat_statements** — 查询统计扩展
- **hypopg** — 假设索引扩展
- **pg_qualstats** — 查询条件统计
- **PoWA** — PostgreSQL 工作负载分析器
