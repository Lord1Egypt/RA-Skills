# 10khr May 2026 — Batch Critique of 40 Skills

## Key Scoring Insights

**Scoring is extremely strict.** To reach 45/50, need near-perfect scores across ALL 9 rated dimensions. Every dimension at 4 = 36. Need 4-5 dimensions at 5 to cross 45.

**Exact-case headings matter.** `## When to Use` not `## When to use`. `## When NOT to Use` not `## When not to use`. `## Gotchas` not `## Common Pitfalls`.

**Code ratio** = fenced code lines / total lines. Target: under 20%. Move large code blocks (dir trees, bulk sync scripts) to references.

## Fixes That Push 42 → 45

Skills at 42 have all dimensions at 4. The fix pattern:
1. Add `## Freedom Calibration` (D6: 4→5)
2. Add `## When NOT to Use` (D10: 4→5)
3. Ensure description has NOT clause AND "when" triggers (D2: 4→5)

## Freedom Calibration Templates

OCAS skills:
```
## Responsibility Boundary
{skill-name} owns its core domain operations.
{skill-name} does not own: trigger detection, session management, or cross-skill orchestration.
```

Util skills:
```
## Freedom Calibration
Fragile operations (API calls, destructive changes) use exact commands. Flexible tasks provide defaults but allow overrides.
```