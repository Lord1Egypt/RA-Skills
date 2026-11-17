# Architecture

## Four memory layers

| Layer | Path | Retention | Content |
|---|---|---|---|
| Short · raw | `short/raw/` | 30d → gz | raw message stream |
| Short · working | `short/working/` | real-time | tasks / decisions / questions |
| Medium | `medium/` | 180d → gz | daily topic summaries |
| Long-term | `MEMORY.md` | permanent | global prefs / facts |

## Pipeline

```
user message → hook → record (IMP score, tags) → JSONL
  high-imp → recall → compoundScore → last-recall.json
  every 30min / 8 high-imp → consolidate → medium blocks + index
  nightly 22:30 → distill → proposals → MEMORY.md (human approve)
```

## Compound-cue scoring

`0.35·imp + 0.25·recency + 0.25·keyword + 0.10·hitFreq + 0.05·layerW`

plus cognitive effects: primacy, RIF penalty, testing boost, Zeigarnik signal, context bonus.
