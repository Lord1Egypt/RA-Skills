# Baseline profiles for Graph Memory Zero

Use these as preset targets. Apply only under `plugins.entries.graph-memory.config.recallPolicy`.

## 1) Balanced (default)

Best for most production cases.

```json
{
  "threshold": 0.62,
  "infer": true,
  "filters": { "memoryType": "all" },
  "preferenceLexicon": {
    "version": "2026-03-27.balance-v1",
    "enabled": true,
    "keywords": [
      "preference", "prefer", "like", "default", "style", "habit",
      "偏好", "喜欢", "默认", "风格", "习惯", "倾向", "口味"
    ],
    "notes": "Balanced default profile for recall governance"
  }
}
```

## 2) Precision-first

Use when false positives are high.

```json
{
  "threshold": 0.68,
  "infer": true,
  "filters": { "memoryType": "fact" },
  "preferenceLexicon": {
    "version": "2026-03-27.precision-v1",
    "enabled": true,
    "keywords": ["preference", "prefer", "偏好", "默认"],
    "notes": "Higher precision with stricter threshold and narrower memoryType"
  }
}
```

## 3) Recall-first

Use when misses are high (but monitor noise).

```json
{
  "threshold": 0.56,
  "infer": true,
  "filters": { "memoryType": "all" },
  "preferenceLexicon": {
    "version": "2026-03-27.recall-v1",
    "enabled": true,
    "keywords": [
      "preference", "prefer", "like", "default", "style", "habit", "tendency",
      "偏好", "喜欢", "默认", "风格", "习惯", "倾向", "口味", "常用"
    ],
    "notes": "Higher recall baseline; verify off-topic inflation"
  }
}
```

## Conflict rule

If `threshold` and legacy `minScore` both exist:

- `effectiveThreshold = max(threshold, minScore)`
- Report this explicitly in every optimization summary.

## Patch style

- Prefer smallest patch containing only changed keys.
- Avoid touching unrelated plugin sections.
- Keep `before` and `after` snapshots for rollback.
