# Context Guard — quickstart

```bash
python scripts/self_check.py
python scripts/context_guard.py demo

# Real tool dump
python scripts/context_guard.py toolpack --file ./my_tool_result.txt --budget 4000
```

Agent rule of thumb:

> Never re-inject a tool dump over ~4k tokens without running `toolpack` first.
