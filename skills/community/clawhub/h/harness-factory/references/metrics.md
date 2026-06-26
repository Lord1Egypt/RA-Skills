# Harness Engineering Metrics

## Purpose
Track the quality and efficiency of the Harness workflow over time. 
Like AutoResearch — hard metrics let us see continuous improvement.

## Per-Sprint Metrics (record after every sprint)

### Efficiency Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **Rounds to Pass** | How many Build→Review rounds needed | ≤ 2 |
| **Time to Ship** | Total wall-clock time from SPRINT.md to deploy | ≤ 1 hour |
| **First-Round Score** | Builder's score on Round 1 | ≥ 6/10 |
| **Final Score** | Score when shipped | ≥ 7.5/10 |
| **Score Improvement** | Final score - First round score | > 0 |

### Quality Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **Critical Bugs Caught** | Bugs that would break production | Track (lower = better SPRINT.md) |
| **Post-Deploy Bugs** | Bugs found AFTER shipping | 0 |
| **Compile Pass Rate** | % of rounds where all files compile | 100% |
| **Security Issues Found** | Found during review | Track (lower = better Builder) |

### SPRINT.md Quality Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **Criteria Completeness** | % of success criteria met on Round 1 | ≥ 80% |
| **Scope Violations** | Builder changed files outside scope | 0 |
| **Context Sufficiency** | Builder asked clarifying questions | 0 (means SPRINT was clear) |

## Tracking Table

Copy this table to HARNESS_METRICS.md in your workspace and update after each sprint:

```markdown
| Date | Sprint | Rounds | Time | R1 Score | Final | Critical Bugs | Post-Deploy |
|------|--------|--------|------|----------|-------|---------------|-------------|
| 2026-03-28 | Brand Style Clone | 5 | 3h | B+(6.5) | A+(9) | 2 (CORS, SSRF) | 0 |
| 2026-03-28 | TrendMuse Upgrade | 4 | 2.5h | audit | A(8) | 1 (URL routing) | 0 |
| 2026-03-29 | TM Data Migration | 1 | 6min | 8.1 | 8.1 | 0 | TBD |
```

## Trend Analysis

After 10+ sprints, analyze:
1. **Is first-round score improving?** → Builder learning from better SPRINTs
2. **Is rounds-to-pass decreasing?** → System getting more efficient
3. **Is critical bugs per sprint decreasing?** → Preventive checks working
4. **Which dimension scores lowest?** → Focus area for checklist improvement

## AutoResearch Connection

This metrics system enables recursive self-improvement:
```
Sprint N → Record metrics → Analyze trends → 
  → Improve SPRINT template / checklists / prompts → 
    → Sprint N+1 (should score higher)
```

The Harness system itself evolves through its own feedback loop.
