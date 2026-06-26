# PRIORITIZATION ENGINE

Always work on the highest-value task next.

---

## PRIORITY ORDER (STRICT)

1. Security issues (any severity)
2. Failing tests
3. Correctness bugs
4. Missing features (with a spec)
5. Performance improvements
6. Refactoring / debt reduction
7. Documentation gaps

**Never skip a higher-priority item to work on a lower one.**

---

## SCORING FORMULA

```
task_score = impact x severity x frequency
```

| Factor | Low | Medium | High | Critical |
|--------|-----|--------|------|----------|
| Impact | 1 | 2 | 3 | 4 |
| Severity | 1 | 2 | 3 | 4 |
| Frequency | 1 | 2 | 3 | 4 |

Maximum score: 64 (critical x critical x critical)

---

## SCORING RULES
- Security issues: always score >= 48 regardless of frequency.
- Failing tests: always score >= 36.
- Tasks without a spec: cannot be scored; create spec first.

---

## SELECTION RULE
Select the top N tasks by score where N <= `CONFIG.yaml => runtime.max_parallel_agents`.
Ties are broken by: security > correctness > reliability > performance.
