# PRISM Archive Retention Policy

## Current State (2026-03-18)
- Archive location: `analysis/prism/archive/`
- Growth rate: ~30KB/day at current usage
- 6-month projection: ~5.4MB (manageable)

## Retention Schedule

| Age | Action |
|-----|--------|
| < 1 year | Keep full findings files |
| 1–2 years | Compress to `archive-YYYY.tar.gz`, keep index |
| > 2 years | Delete raw findings; keep summary index only |

## Size Limits

- Max per topic directory: 20MB
- If exceeded: compress oldest reviews first
- Max total archive: 500MB (alert if approaching)

## Index Format

When compressing, preserve a summary index:
```markdown
# PRISM Archive Index — <topic-slug>
| Date | Verdict | Key Findings | Full Archive |
|------|---------|-------------|-------------|
| YYYY-MM-DD | AWC | [1-line summary] | archive-YYYY.tar.gz |
```

## Automation (Future)

A cron job to enforce this policy doesn't exist yet. Until it does, run manually:
```bash
# Check archive size
du -sh ~/.openclaw/agents/main/workspace/analysis/prism/archive/

# Find old reviews
find ~/.openclaw/agents/main/workspace/analysis/prism/archive/ -name "*.md" -mtime +365
```
