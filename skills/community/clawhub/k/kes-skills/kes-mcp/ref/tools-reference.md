# KingbaseES MCP Server 工具详解

本文档详细描述 kingbase-mcp 提供的所有工具，包括参数、返回值和使用场景。

---

## 1. list_schemas — 列出所有模式

列出数据库中所有的 schema。

### 参数

无参数。

### 返回值

数组，每个元素包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| `schema_name` | string | 模式名称 |
| `schema_owner` | string | 模式所有者 |
| `schema_type` | string | 类型：System Schema / System Information Schema / User Schema |

### 示例

```
# 调用
list_schemas()

# 返回示例
[
    ["information_schema", "SYSTEM", "System Information Schema"],
    ["sys", "SYSTEM", "System Schema"],
    ["public", "SYSTEM", "System Schema"],
    ["my_app", "MY_USER", "User Schema"]
]
```

### 使用场景

- 探索数据库结构的第一步
- 确认已部署的自定义 schema

---

## 2. list_objects — 列出模式中的对象

列出指定 schema 中的表、视图、序列或扩展。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `schema_name` | string | 是 | — | 模式名称 |
| `object_type` | string | 否 | `"table"` | 对象类型：`"table"`, `"view"`, `"sequence"`, `"extension"` |

### 返回值

数组，对象类型不同返回的字段不同：

**表/视图**:
| 字段 | 说明 |
|------|------|
| `schema` | 模式名称 |
| `name` | 对象名称 |
| `type` | `BASE TABLE` 或 `VIEW` |

**序列**:
| 字段 | 说明 |
|------|------|
| `schema` | 模式名称 |
| `name` | 序列名称 |
| `data_type` | 数据类型 |

**扩展**:
| 字段 | 说明 |
|------|------|
| `name` | 扩展名称 |
| `version` | 扩展版本 |
| `relocatable` | 是否可迁移 |

### 示例

```
# 列出 public schema 的表
list_objects(schema_name="public", object_type="table")

# 返回示例
[
    {"schema": "public", "name": "users", "type": "BASE TABLE"},
    {"schema": "public", "name": "orders", "type": "BASE TABLE"}
]
```

### 使用场景

- 获取某个 schema 下的所有表
- 检查已安装的扩展列表
- 排查序列定义

---

## 3. get_object_details — 获取对象详情

获取指定数据库对象的详细信息，包括列、约束、索引等。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `schema_name` | string | 是 | — | 模式名称 |
| `object_name` | string | 是 | — | 对象名称 |
| `object_type` | string | 否 | `"table"` | 对象类型：`"table"`, `"view"`, `"sequence"`, `"extension"` |

### 返回值

**表/视图**:
```json
{
    "basic": {
        "schema": "public",
        "name": "users",
        "type": "BASE TABLE"
    },
    "columns": [
        {
            "column": "id",
            "data_type": "integer",
            "is_nullable": "NO",
            "default": "nextval('users_id_seq'::regclass)"
        }
    ],
    "constraints": [
        {"name": "users_pkey", "type": "PRIMARY KEY", "columns": ["id"]}
    ],
    "indexes": [
        {"name": "users_pkey", "definition": "CREATE UNIQUE INDEX..."}
    ]
}
```

**序列**: 包含 `schema`、`name`、`data_type`、`start_value`、`increment`

**扩展**: 包含 `name`、`version`、`relocatable`

### 使用场景

- SQL 编写前了解表结构
- 排查索引覆盖情况
- 查看约束定义

---

## 4. execute_sql — 执行 SQL

执行 SQL 查询。此工具的行为取决于访问模式。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sql` | string | 是 | — | SQL 语句 |

### 模式差异

| 模式 | 行为 |
|------|------|
| `restricted`（默认） | 仅允许 SELECT 查询，30 秒超时 |
| `unrestricted` | 允许任意 SQL（INSERT/UPDATE/DELETE/DML/DDL） |

### 返回值

数组，每行数据为字典（列名 → 值）。若无结果则返回 `None`。

### 示例

```
# 执行查询
execute_sql(sql="SELECT id, name, email FROM public.users LIMIT 5")

# 返回示例
[
    {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "email": "lisi@example.com"}
]
```

### 注意事项

- Restricted 模式会校验 SQL，非 SELECT 语句将报错
- 查询结果可能很大，建议添加 LIMIT
- 密码在日志中会被脱敏

---

## 5. explain_query — 执行计划分析

分析 SQL 的执行计划，支持假设索引模拟。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sql` | string | 是 | — | 待分析的 SQL |
| `analyze` | boolean | 否 | `false` | 是否实际执行查询获取真实统计 |
| `hypothetical_indexes` | list[dict] | 否 | `[]` | 假设索引列表 |

### 假设索引格式

```json
[
    {"table": "users", "columns": ["email"], "using": "btree"},
    {"table": "orders", "columns": ["user_id", "created_at"]}
]
```

### 返回值

文本格式的执行计划，包含节点类型、预估行数、预估成本等。

### 模式说明

- `analyze=false`: 仅预估（默认）
- `analyze=true`: 实际执行并返回真实耗时（不能与 hypothetical_indexes 同时使用）
- `hypothetical_indexes`: 需要 `sys_hypo` 扩展

### 使用场景

- SQL 性能诊断的第一步
- 评估索引优化效果（假设索引模式）
- 对比优化前后的执行计划

---

## 6. analyze_workload_indexes — 工作负载索引分析

基于 `sys_stat_statements` 收集的历史执行数据，分析频繁执行的查询并推荐索引。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `max_index_size_mb` | integer | 否 | `10000` | 单个索引最大大小（MB） |
| `method` | string | 否 | `"dta"` | 分析方法：`"dta"` 或 `"llm"` |

### 分析方法

| 方法 | 说明 |
|------|------|
| `dta` | Database Tuning Advisor，基于统计数据的确定性分析 |
| `llm` | LLM 辅助分析，结合大语言模型建议 |

### 返回值

文本格式的索引建议报告，包含：
- 当前工作负载分析
- 推荐创建的索引
- 预估性能提升

### 前置条件

- 需要 `sys_stat_statements` 扩展已安装
- 数据库需积累一定执行历史

### 使用场景

- 生产环境索引优化
- 定期索引健康审计

---

## 7. analyze_query_indexes — 指定 SQL 索引分析

针对指定的 SQL 查询列表推荐最优索引。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `queries` | list[string] | 是 | — | SQL 查询列表（最多 10 条） |
| `max_index_size_mb` | integer | 否 | `10000` | 索引最大大小 |
| `method` | string | 否 | `"dta"` | 分析方法：`"dta"` 或 `"llm"` |

### 约束

- `queries` 至少 1 条，最多 10 条

### 返回值

文本格式的分析报告，每条 SQL 对应独立的索引建议。

### 使用场景

- 针对特定慢查询进行优化
- 新上线 SQL 的索引预评估

---

## 8. analyze_db_health — 数据库健康检查

全面检查数据库健康状况。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `health_type` | string | 否 | `"all"` | 检查类型，逗号分隔 |

### 支持的检查类型

| 类型 | 说明 |
|------|------|
| `index` | 无效索引、重复索引、膨胀索引 |
| `connection` | 连接数和利用率 |
| `vacuum` | 事务 ID 回绕风险 |
| `sequence` | 序列溢出风险 |
| `replication` | 复制延迟和复制槽 |
| `buffer` | 缓冲池命中率（表和索引） |
| `constraint` | 无效约束 |
| `all` | 运行所有检查 |

### 返回值

文本格式的健康报告，包含每个检查项的状态、警告和建议。

### 使用场景

- 日常巡检
- 故障排查前的全面检查

---

## 9. get_top_queries — 获取 TOP N 慢查询

基于 `sys_stat_statements` 获取最耗时的查询。

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sort_by` | string | 否 | `"resources"` | 排序依据 |
| `limit` | integer | 否 | `10` | 返回数量（仅 `total_time` / `mean_time` 模式下有效） |

### 排序方式

| 值 | 说明 |
|---|------|
| `total_time` | 按总执行时间排序 |
| `mean_time` | 按平均执行时间排序 |
| `resources` | 按资源消耗排序（推荐） |

### 返回值

文本格式的慢查询报告，包含 SQL、执行次数、总耗时、平均耗时、行数等。

### 前置条件

需要 `sys_stat_statements` 扩展已安装。

### 使用场景

- 慢查询定位
- 资源消耗分析
- SQL 优化优先级排序

---

## 工具汇总

| 工具 | 参数数 | 访问模式 | 主要用途 |
|------|--------|---------|---------|
| `list_schemas` | 0 | 只读 | 结构探索 |
| `list_objects` | 2 | 只读 | 结构探索 |
| `get_object_details` | 3 | 只读 | 结构探索 |
| `execute_sql` | 1 | 受限/不限 | SQL 执行 |
| `explain_query` | 3 | 只读 | 执行计划 |
| `analyze_workload_indexes` | 2 | 只读 | 索引优化 |
| `analyze_query_indexes` | 3 | 只读 | 索引优化 |
| `analyze_db_health` | 1 | 只读 | 健康检查 |
| `get_top_queries` | 2 | 只读 | 慢查询分析 |
