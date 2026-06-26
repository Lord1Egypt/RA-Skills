# HARNESS SELF-ASSESSMENT

Per-cycle evaluation of harness effectiveness. The harness measures itself.

## PURPOSE

The harness is a searchable artifact (Meta-Harness principle). To improve it,
we must first measure it. This protocol produces a per-cycle health score that
feeds into the feedback closed-loop.

## ASSESSMENT CHECKLIST (5 questions, scored 0-5 each)

### Q1: Gap Resolution Effectiveness (0-5)
  5 = All planned gaps closed, no regressions, no new gaps introduced
  3 = Most gaps closed, minor regressions fixed in same cycle
  1 = Few gaps closed, multiple regressions or new gaps
  0 = Net negative: more gaps opened than closed

### Q2: Context Efficiency (0-5)
  5 = Avg context tokens per gap within budget (see EFFICIENCY-HISTORY.md)
  3 = Slightly over budget but trending down
  1 = Significantly over budget, context bloat detected
  0 = Context exhaustion forced multiple resets per gap

### Q3: Agent Discipline (0-5)
  5 = All agents stayed within tool subsets, no permission violations
  3 = Minor violations caught and corrected by tool router
  1 = Multiple tool subset violations, agents needed redirection
  0 = Agents repeatedly violated constraints despite reminders

### Q4: Human Gate Compliance (0-5)
  5 = All gates respected, human acknowledged each one
  3 = All gates surfaced but some with delays or format issues
  1 = Gates missed or bypassed without human acknowledgment
  0 = Critical gate (plan approval, architecture change) skipped

### Q5: Entropy Trend (0-5)
  5 = Entropy score decreased (dead code removed, docs updated, tests added)
  3 = Entropy stable (no increase, some cleanup done)
  1 = Entropy increased slightly (new tech debt, some stale docs)
  0 = Entropy increased significantly (codebase degradation)

## SCORING

Aggregate score: sum of Q1-Q5 (range: 0-25)

| Score | Status | Action |
|-------|--------|--------|
| 20-25 | Healthy | Continue as-is. Log score in EFFICIENCY-HISTORY.md. |
| 15-19 | Attention | Log score. Review Q with lowest score. Surface to human. |
| 10-14 | Concern | Log score. Review all low-Q items. Recommend harness variant search. |
| 0-9  | Critical | HALT. Surface full assessment to human. Do NOT start next cycle. |

## TREND TRACKING

Append to docs/status/EFFICIENCY-HISTORY.md after each cycle:
```
CYCLE-NNN Self-Assessment: QQ/25
  Q1 (gaps): N  Q2 (context): N  Q3 (discipline): N  Q4 (gates): N  Q5 (entropy): N
  Trend: ↑ stable ↓ (vs last cycle aggregate)
  Action: <none | review | variant-search | halt>
```

## TRIGGER FOR HARNESS-VARIANT SEARCH

If aggregate score < 15 for 2 consecutive cycles:
→ Automatically trigger harness-variant search (runtime/self-improvement.md Part 3)
→ Surface to human with specific improvement proposals
