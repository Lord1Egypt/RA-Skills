# 📄 `01_minimal_3_lines.py`

**Path:** `/mnt/Morgana/skills/morgana-anti-infinite-loop-v2-en/examples/01_minimal_3_lines.py`  
**Size:** 1,124 bytes / 34 lines  
**Hash:** `ee321a8b69c1e094`  
**Generated:** 2026-06-09T01:00:46.594200+00:00

## 📝 Module Docstring

```
🌀 Example 1: Minimal 3-line integration (dev solo + Llama local).

Le cas le plus simple : un agent qui retry la même action.
Tu wrap ton agent avec le guard, et c'est tout.
```

## 📦 Imports (1)

```python
import anti_loop.AntiLoop
```

## ⚡ Functions (1)

### `def fake_agent_loop(state, action):`
> A minimal agent stub: returns whatever was asked, every time.
