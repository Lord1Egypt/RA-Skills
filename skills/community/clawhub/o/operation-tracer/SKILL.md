---
name: operation-tracer
version: 1.0.0
description: "SQLite 操作追踪系统。记录所有工具调用、LLM调用、错误和压缩操作，供事后分析和性能优化。"
---

# Operation Tracer

## 功能
- 追踪所有操作（工具调用、LLM调用、错误、压缩）
- SQLite 持久化存储
- 性能分析（慢操作、错误统计）
- 数据导出（JSON/CSV）
- 自动清理旧数据

## 使用方法

```python
from tracer import OperationTracer
from analyzer import TraceAnalyzer

# 追踪操作
tracer = OperationTracer()
span_id = tracer.start_span("read_file", "tool_call", {"path": "/tmp/test"})
# ... 执行操作 ...
tracer.end_span(span_id, result="success", status="success")

# 分析数据
analyzer = TraceAnalyzer()
summary = analyzer.get_summary()
slow_ops = analyzer.get_slow_operations(threshold_ms=1000)
errors = analyzer.get_error_operations()
```

## 追踪内容

| 类型 | 说明 | 元数据示例 |
|------|------|-----------|
| tool_call | 工具调用 | 名称、参数、耗时、结果、状态 |
| llm_call | LLM 调用 | token 消耗、响应时间 |
| error | 错误和重试 | 错误类型、重试次数 |
| compression | 上下文压缩 | 压缩前后 token 数 |

## 集成点

- **hook-engine** PreToolUse Hook → `start_span()`
- **hook-engine** PostToolUse Hook → `end_span()`
- **self-improving** → 数据分析（`get_summary()` / `get_error_operations()`）

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/tracer.py` | 追踪器核心（OperationTracer） |
| `scripts/analyzer.py` | 数据分析器（TraceAnalyzer） |
| `scripts/test_tracer.py` | 测试用例 |

## 存储

SQLite 数据库路径：`traces/agent_traces.db`（相对于 workspace）

表结构详见 `references/trace_schema.md`。
