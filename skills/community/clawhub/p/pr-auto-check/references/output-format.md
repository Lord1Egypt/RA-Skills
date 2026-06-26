# PR Auto-Check Output Format

## JSON Schema

```json
{
  "timestamp": "ISO-8601 UTC",
  "pr": 42,
  "ci": {
    "pass": true,
    "summary": "All checks passed"
  },
  "diff_stats": "5 files changed, 120 insertions(+), 30 deletions(-)",
  "changed_files": ["src/main.py", "tests/test_main.py"],
  "health": {
    "max_severity": 0,
    "summary": "postgres: ok, nginx: ok, disk: ok",
    "raw": { "timestamp": "...", "max_severity": 0, "checks": {} }
  }
}
```

## Severity Levels

| max_severity | Status | Discord Color |
|-------------|--------|---------------|
| 0 | All healthy | Green (3066993) |
| 1 | Warnings | Yellow (16776960) |
| 2+ | Critical | Red (15158332) |
