# Memory Template — Nginx

Create `~/Clawic/data/nginx/memory.md` with this structure:

```markdown
# Nginx Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- What nginx fronts: PHP-FPM, Node, containers, static -->
<!-- Config layout in use, LB/CDN in front, TLS setup -->

## Incidents
<!-- Problems already debugged and their root causes -->

## Preferences
<!-- Verbose explanations vs quick directives -->
<!-- Rollout caution (302-first, HSTS ramp) vs move fast -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their setup |
| `complete` | Know their stack well |
