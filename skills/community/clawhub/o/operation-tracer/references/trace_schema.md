# Trace Schema - 数据库表结构说明

## traces 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | TEXT PRIMARY KEY | 追踪跨度ID（8位UUID前缀） |
| timestamp | REAL NOT NULL | 操作开始时间（Unix时间戳） |
| operation_type | TEXT | 操作类型：tool_call / llm_call / error / compression |
| operation_name | TEXT | 操作名称（如 read_file、web_search） |
| duration_ms | REAL | 操作耗时（毫秒） |
| metadata | TEXT | JSON格式的附加元数据 |
| result | TEXT | 操作结果（字符串化） |
| status | TEXT | 状态：running / success / error |

## 操作类型说明

### tool_call
工具调用追踪。元数据示例：
```json
{
  "operation_type": "tool_call",
  "tool_name": "read",
  "parameters": {"path": "/tmp/test.md"}
}
```

### llm_call
LLM 调用追踪。元数据示例：
```json
{
  "operation_type": "llm_call",
  "model": "qwen3.7-plus",
  "input_tokens": 1500,
  "output_tokens": 800
}
```

### error
错误和重试追踪。元数据示例：
```json
{
  "operation_type": "error",
  "error_type": "TimeoutError",
  "retry_count": 3,
  "original_span_id": "abc12345"
}
```

### compression
上下文压缩追踪。元数据示例：
```json
{
  "operation_type": "compression",
  "tokens_before": 50000,
  "tokens_after": 20000,
  "compression_ratio": 0.6
}
```

## 数据库位置

默认路径：`traces/agent_traces.db`（相对于 workspace 根目录）
