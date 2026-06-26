---
name: debugging
description: Debugging assistant. Analyzes error logs, suggests breakpoints, traces execution flow, and helps identify root causes of issues.
---

# Debugging Assistant

调试助手，分析错误日志、建议断点、追踪执行流程、帮助识别问题根因。

**Version**: 1.1  
**Features**: 错误分析、断点建议、执行追踪、根因分析、C/C++ 支持 (NEW)

---

## Quick Start

### 1. 分析错误日志

```bash
# 分析 Python 错误
python3 scripts/main.py analyze-error "Traceback (most recent call last):..."

# 从文件分析
python3 scripts/main.py analyze-error --file error.log
```

### 2. 建议断点

```bash
# 为代码建议断点位置
python3 scripts/main.py suggest-breakpoints --file src/main.py

# 针对特定函数
python3 scripts/main.py suggest-breakpoints --function process_data
```

### 3. 追踪执行

```bash
# 追踪函数调用
python3 scripts/main.py trace --file src/app.py --function handle_request
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `analyze-error` | 分析错误 | `analyze-error "Traceback..."` |
| `suggest-breakpoints` | 建议断点 | `suggest-breakpoints --file src.py` |
| `trace` | 追踪执行 | `trace --file src.py --function foo` |

---

## Error Analysis

### Python Traceback 分析

```bash
$ python3 scripts/main.py analyze-error "Traceback (most recent call last):
  File 'src/auth.py', line 45, in login
    user = db.get_user(username)
  File 'src/db.py', line 23, in get_user
    cursor.execute(query, (username,))
psycopg2.OperationalError: connection closed"

🔍 Error Analysis
=================

Type: Database Connection Error
Severity: 🔴 High

Root Cause:
The database connection was closed before executing the query.

Possible Causes:
1. Connection pool exhaustion
2. Connection timed out
3. Database server restart

Suggested Fixes:
1. Check connection pool settings
2. Implement connection retry logic
3. Add connection health checks

File: src/db.py:23
Function: get_user
```

### 常见错误模式

自动识别：
- `ImportError` / `ModuleNotFoundError` - 导入问题
- `AttributeError` - 属性访问错误
- `KeyError` / `IndexError` - 数据访问错误
- `TypeError` - 类型错误
- `ConnectionError` - 网络/连接错误
- `TimeoutError` - 超时错误

---

## Breakpoint Suggestions

```bash
$ python3 scripts/main.py suggest-breakpoints --file src/payment.py

🔍 Breakpoint Suggestions
=========================

High Priority:
  Line 45: process_payment() - Entry point
  Line 67: validate_card() - Validation logic
  Line 89: charge_customer() - External API call

Medium Priority:
  Line 34: calculate_total() - Business logic
  Line 56: apply_discount() - Conditional logic

Tips:
- Set breakpoints before external API calls
- Watch variables: amount, currency, customer_id
```

---

## Execution Tracing

```bash
$ python3 scripts/main.py trace --file src/api.py --function handle_request

🔍 Execution Trace
==================

Function: handle_request
File: src/api.py:23

Call Graph:
handle_request
├── authenticate_user
│   └── verify_token
├── validate_request
│   └── check_schema
├── process_data
│   ├── fetch_from_db
│   └── cache_result
└── format_response

Potential Issues:
- No error handling in process_data
- External call to fetch_from_db (line 67)
```

---

## Configuration

`.debugging.json`:

```json
{
  "breakpoints": {
    "before_external_calls": true,
    "before_conditionals": true,
    "in_error_handlers": true
  },
  "error_patterns": {
    "ignore": ["DeprecationWarning"],
    "highlight": ["SecurityError", "DataLossError"]
  }
}
```

---

## Examples

### 场景 1：排查崩溃问题

```bash
# 1. 复制错误信息
python3 main.py analyze-error "$(cat error.log)"

# 2. 根据分析设置断点
python3 main.py suggest-breakpoints --file src/crash_point.py

# 3. 追踪相关函数
python3 main.py trace --function problematic_function
```

### 场景 2：性能问题排查

```bash
# 追踪执行路径
python3 main.py trace --file src/slow_endpoint.py --function handler

# 识别冗余调用
```

### 场景 3：API 错误调试

```bash
# 分析 API 错误响应
python3 main.py analyze-error "HTTP 500: Internal Server Error"

# 检查 API 处理代码
python3 main.py suggest-breakpoints --file src/api/handlers.py
```

---

## Files

```
skills/debugging/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── error_analyzer.py       # 错误分析器
    └── tracer.py               # 执行追踪器
```

---

## Roadmap

- [x] Python error analysis
- [ ] JavaScript error analysis
- [ ] Interactive debugger integration
- [ ] Log file monitoring
