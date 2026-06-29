# 📄 `02_pre_flight_regex.py`

**Path:** `/mnt/Morgana/skills/morgana-anti-infinite-loop-v2-en/examples/02_pre_flight_regex.py`  
**Size:** 986 bytes / 32 lines  
**Hash:** `075d2b965cec52bd`  
**Generated:** 2026-06-09T01:00:46.594635+00:00

## 📝 Module Docstring

```
🌀 Example 2: Pre-flight plan check (0 LLM, 0 token).

Avant même d'exécuter un plan, on vérifie s'il contient un pattern
de boucle. Aucune appel LLM, c'est du regex.
```

## 📦 Imports (1)

```python
import anti_loop.AntiLoop
```

## ⚡ Functions (1)

### `def looks_like_a_loop(plan):`
> Detect: does this plan look like it could loop forever?
