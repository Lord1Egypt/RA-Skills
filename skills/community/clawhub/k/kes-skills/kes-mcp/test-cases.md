# KingbaseES MCP Server 测试用例

## 测试环境

- KingbaseES V9 容器（端口 54321）
- 连接 URL: `kingbase://SYSTEM:12345678ab@localhost:54321/test`
- MCP Server 版本: v0.3.0

---

## 1. 基本连接测试

### 1.1 启动 MCP Server

```bash
# Stdio 模式（默认）
DATABASE_URI="kingbase://SYSTEM:12345678ab@localhost:54321/test" \
  uv run kingbase-mcp

# SSE 模式
DATABASE_URI="kingbase://SYSTEM:12345678ab@localhost:54321/test" \
  uv run kingbase-mcp --transport sse --sse-port 8000

# Streamable HTTP 模式
DATABASE_URI="kingbase://SYSTEM:12345678ab@localhost:54321/test" \
  uv run kingbase-mcp --transport streamable-http --streamable-http-port 8000
```

**预期**: Server 正常启动，无报错

---

## 2. 工具测试

### 2.1 list_schemas

```
调用: list_schemas()
```

**预期返回**: 包含 `information_schema`、`sys`、`public` 等 schema 的列表

### 2.2 list_objects

```
调用: list_objects(schema_name="public", object_type="table")
```

**预期返回**: public schema 下所有 BASE TABLE 的列表，每行包含 `schema`、`name`、`type`

### 2.3 get_object_details

```
调用: get_object_details(schema_name="public", object_name="test_table", object_type="table")
```

**预期返回**: 包含 `columns`、`constraints`、`indexes` 的详情

### 2.4 execute_sql（Restricted 模式）

```
调用: execute_sql(sql="SELECT count(*) FROM sys_tables")
```

**预期返回**: 包含计数的结果行

**错误测试**: 尝试执行非 SELECT 语句
```
调用: execute_sql(sql="INSERT INTO test_table VALUES (1)")
```
**预期**: 报错，提示 restricted 模式不允许

### 2.5 execute_sql（Unrestricted 模式）

启动时使用 `--access-mode unrestricted`：

```
调用: execute_sql(sql="CREATE TABLE IF NOT EXISTS test_mcp (id INT PRIMARY KEY, name VARCHAR(50))")
调用: execute_sql(sql="INSERT INTO test_mcp VALUES (1, 'test')")
调用: execute_sql(sql="SELECT * FROM test_mcp")
调用: execute_sql(sql="DROP TABLE test_mcp")
```

**预期**: 所有操作正常执行

### 2.6 explain_query

```
调用: explain_query(sql="SELECT * FROM sys_tables WHERE tablename = 'test'")
```

**预期返回**: 文本格式的执行计划，包含 Seq Scan 或 Index Scan 节点

### 2.7 explain_query（假设索引）

```
调用: explain_query(
    sql="SELECT * FROM users WHERE email = 'test@example.com'",
    hypothetical_indexes=[{"table": "users", "columns": ["email"], "using": "btree"}]
)
```

**预期**: 若 `sys_hypo` 已安装，返回含假设索引的执行计划；若未安装，提示需安装扩展

### 2.8 analyze_workload_indexes

```
调用: analyze_workload_indexes(max_index_size_mb=1000, method="dta")
```

**预期**: 返回基于 `sys_stat_statements` 的索引建议报告

**前置条件**: `sys_stat_statements` 扩展已安装且有查询历史

### 2.9 analyze_query_indexes

```
调用: analyze_query_indexes(
    queries=["SELECT * FROM users WHERE age > 18 AND city = 'Beijing'"],
    max_index_size_mb=100,
    method="dta"
)
```

**预期**: 返回针对该 SQL 的索引建议

### 2.10 analyze_db_health

```
调用: analyze_db_health(health_type="all")
```

**预期**: 返回包含 index/connection/vacuum/sequence/replication/buffer/constraint 的完整健康报告

**单检查项测试**:
```
调用: analyze_db_health(health_type="index")
```
**预期**: 仅返回索引检查结果

### 2.11 get_top_queries

```
调用: get_top_queries(sort_by="resources")
调用: get_top_queries(sort_by="mean_time", limit=5)
```

**预期**: 返回资源消耗最大或平均耗时最长的查询列表

---

## 3. 集成测试流程

模拟 AI 助手使用 MCP Server 的完整流程：

```
步骤 1: list_schemas()                          → 获取所有 schema
步骤 2: list_objects("public", "table")          → 获取表列表
步骤 3: get_object_details("public", "users")   → 了解 users 表结构
步骤 4: execute_sql("SELECT * FROM users LIMIT 3") → 查看数据
步骤 5: explain_query("SELECT * FROM users WHERE email = 'x@y.com'") → 分析执行计划
步骤 6: analyze_query_indexes([上述SQL])         → 获取索引建议
步骤 7: execute_sql("CREATE INDEX...")           → 应用建议（unrestricted 模式）
步骤 8: explain_query(同上SQL)                   → 验证执行计划改善
步骤 9: analyze_db_health("all")                 → 全面健康检查
步骤 10: get_top_queries("resources")            → 慢查询排查
```

---

## 4. 异常测试

| 测试项 | 操作 | 预期 |
|--------|------|------|
| 无数据库 URL | 不设置 DATABASE_URI 且无命令行参数 | 报错提示 "No database URL provided" |
| 错误 URL | 使用错误的连接字符串 | 警告日志 "Could not connect to database"，Server 仍可启动 |
| 超长查询 | 执行超过 30 秒的查询（restricted 模式） | 超时错误 |
| 空 queries | `analyze_query_indexes(queries=[])` | 报错 "non-empty list of queries" |
| 超限 queries | `analyze_query_indexes(queries=[...11 条])` | 报错 "up to 10 queries" |

---

## 5. Claude Code 集成测试

在 `.claude/CLAUDE.md` 配置 kingbase-mcp 后：

1. 在 Claude Code 中询问："列出当前数据库的所有 schema"
2. 预期：Claude Code 自动调用 `list_schemas` 工具并返回结果
3. 询问："分析这条 SQL 的执行计划: SELECT * FROM users WHERE email = 'test@example.com'"
4. 预期：Claude Code 调用 `explain_query` 工具
