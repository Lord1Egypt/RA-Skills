# krea-image-api v1.0.2

Krea.ai skill w/ **Nano Banana 2 default**, full Nano variants.

**Models:**

[table same as SKILL_MD]

## Setup
```jsonc
"KREA_API_TOKEN": "token"
```

## NEW: Rate limits
- Submit jobs: 1/10s
- Poll: 6s intervals, max 40
- Handles 429s gracefully

## Publish
```bash
clawhub publish . \
  --version 1.0.2 \
  --changelog "v1.0.2: Rate limits, 6s polls (15-120s gens), 429 handling, timeouts"
```

MIT.
