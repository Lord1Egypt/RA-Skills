---
name: meta-debugger
description: AI-powered self-debugging system that identifies, analyzes, and fixes errors automatically. Learns from past errors, builds error patterns, generates fix suggestions, and can apply fixes autonomously. Essential capability for self-healing AI systems.
tags:
  - meta
  - debugging
  - error-handling
  - self-healing
  - troubleshooting
  - automation
version: 1.0.0
author: chenq
---

# Meta Debugger

Self-diagnosing and self-healing AI capability.

## Features

### 1. Error Detection
- **Runtime Monitoring**: Detect errors in real-time
- **Pattern Recognition**: Identify error patterns
- **Anomaly Detection**: Find unusual behaviors
- **Log Analysis**: Parse and analyze logs

### 2. Root Cause Analysis
- **Stack Trace Analysis**: Understand error origins
- **Context Tracking**: Track what led to error
- **Similar Errors**: Find related past errors
- **Impact Assessment**: Evaluate error severity

### 3. Fix Generation
- **Solution Suggestions**: Generate fix candidates
- **Code Patches**: Create actual code changes
- **Configuration Fixes**: Fix config issues
- **Workarounds**: Suggest alternative approaches

### 4. Automatic Fix
- **Safe Application**: Apply fixes safely
- **Rollback Support**: Undo if needed
- **Test Validation**: Verify fix works
- **Learning Loop**: Learn from results

### 5. Prevention
- **Pattern Building**: Build error patterns
- **Pre-flight Checks**: Validate before execution
- **Guard Rails**: Add safety checks
- **Monitoring**: Ongoing error watch

## Installation

```bash
pip install json traceback ast
```

## Usage

### Initialize Debugger

```python
from meta_debugger import MetaDebugger

debugger = MetaDebugger(
    name="my_assistant",
    auto_fix=True,
    safe_mode=True
)
```

### Register Error Handlers

```python
@debugger.error_handler
def handle_api_error(error, context):
    """Custom error handler"""
    return {
        'action': 'retry',
        'max_retries': 3,
        'backoff': 'exponential'
    }

@debugger.error_handler  
def handle_timeout(error, context):
    """Handle timeout errors"""
    return {
        'action': 'increase_timeout',
        'new_timeout': 60
    }
```

### Wrap Functions

```python
@debugger.wrap
def call_api(url, params):
    """Function that might fail"""
    return requests.get(url, params=params)
```

### Manual Debug

```python
# Analyze an error
analysis = debugger.analyze(
    error=ValueError("Invalid input"),
    context={'input': user_input, 'function': 'process_data'}
)

print(analysis)
# {
#     'root_cause': 'Type mismatch',
#     'severity': 'medium',
#     'suggestions': [
#         'Convert input to correct type',
#         'Add input validation'
#     ]
# }

# Apply fix
result = debugger.apply_fix(analysis)
```

### Error History

```python
# Get error patterns
patterns = debugger.get_error_patterns()

# Get common fixes
fixes = debugger.get_common_fixes()

# Get prevention suggestions
prevention = debugger.get_prevention_tips()
```

## API Reference

### Error Handling
| Method | Description |
|--------|-------------|
| `@error_handler` | Decorator for error handlers |
| `register_handler(type, handler)` | Register custom handler |
| `handle(error, context)` | Handle an error |

### Analysis
| Method | Description |
|--------|-------------|
| `analyze(error, context)` | Analyze error root cause |
| `get_stack_trace(error)` | Parse stack trace |
| `find_similar(error)` | Find similar past errors |

### Fix Generation
| Method | Description |
|--------|-------------|
| `generate_fixes(error)` | Generate fix candidates |
| `rank_fixes(fixes)` | Rank fixes by probability |
| `apply_fix(fix)` | Apply a fix |

### Prevention
| Method | Description |
|--------|-------------|
| `add_guardrail(check)` | Add pre-execution check |
| `validate_input(input, rules)` | Validate inputs |
| `build_pattern(error)` | Build error pattern |

### Learning
| Method | Description |
|--------|-------------|
| `record_error(error, context)` | Record error for learning |
| `record_fix(error, fix, success)` | Record fix result |
| `get_insights()` | Get learned insights |

## Error Patterns

```python
ERROR_PATTERNS = {
    "timeout": {
        "causes": ["network", "server_load", "query_complexity"],
        "fixes": ["increase_timeout", "retry", "cache"],
        "prevention": ["timeout_guards", "circuit_breaker"]
    },
    "value_error": {
        "causes": ["type_mismatch", "invalid_format", "out_of_range"],
        "fixes": ["type_conversion", "validation", "default_value"],
        "prevention": ["input_validation", "schema_check"]
    },
    "connection_error": {
        "causes": ["network_down", "server_unavailable", "auth_failed"],
        "fixes": ["retry", "reconnect", "fallback"],
        "prevention": ["health_check", "load_balancing"]
    }
}
```

## Fix Strategies

### Retry Strategy
```python
{
    'strategy': 'retry',
    'max_attempts': 3,
    'backoff': 'exponential',
    'backoff_base': 2,
    'max_delay': 60
}
```

### Fallback Strategy
```python
{
    'strategy': 'fallback',
    'primary': 'api_v1',
    'fallback': 'api_v2',
    'condition': 'primary_unavailable'
}
```

### Circuit Breaker
```python
{
    'strategy': 'circuit_breaker',
    'failure_threshold': 5,
    'timeout': 60,
    'half_open_requests': 3
}
```

### Default Value
```python
{
    'strategy': 'default',
    'field': 'result',
    'default': {'status': 'unknown'}
}
```

## Example: Full Usage

```python
from meta_debugger import MetaDebugger

# Initialize
debugger = MetaDebugger("production_assistant")

# Register handlers
@debugger.error_handler
def handle_api_error(error, context):
    if "timeout" in str(error).lower():
        return {'action': 'retry', 'max_retries': 3}
    elif "auth" in str(error).lower():
        return {'action': 'refresh_token'}
    return {'action': 'log_and_continue'}

# Wrap risky function
@debugger.wrap
def fetch_stock_data(symbol):
    # This might fail
    return api.get(f"/stock/{symbol}")

# Use it
try:
    data = fetch_stock_data("600519")
except Exception as e:
    # Debugger automatically handles
    debugger.handle(e, {'function': 'fetch_stock_data', 'symbol': '600519'})
```

## Integration

### With Skills
```python
class MySkill:
    def __init__(self):
        self.debugger = MetaDebugger()
    
    def execute(self, input):
        try:
            return self._execute(input)
        except Exception as e:
            return self.debugger.handle(e, {'skill': 'MySkill', 'input': input})
```

### With OpenClaw
```python
@hookimpl
def on_error(error, context):
    debugger = MetaDebugger()
    return debugger.handle(error, context)
```

## Metrics

| Metric | Description |
|--------|-------------|
| error_rate | Errors per 1000 calls |
| fix_success_rate | Successful fixes |
| avg_recovery_time | Time to recover |
| prevented_errors | Errors caught by guards |

## Best Practices

1. **Start with Safe Mode**: Always review before auto-fixing
2. **Log Everything**: Build learning data
3. **Test Fixes**: Validate before production
4. **Iterate**: Improve patterns over time
5. **Balance**: Don't over-catch or under-catch

## Future Capabilities

- Cross-system error correlation
- AI-generated fixes with LLMs
- Self-healing infrastructure
- Predictive error prevention
