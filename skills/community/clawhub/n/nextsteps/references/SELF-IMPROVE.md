# Self-Improvement Engine

NextSteps uses an Observe → Hypothesize → Experiment → Validate cycle to improve suggestions over time.

## Signal Detection

Track these signals from user behavior after presenting next steps:

| Signal | Detection | Action |
|--------|-----------|--------|
| User selects a suggestion | Message matches or closely relates to a presented suggestion | Log `[SELECTED] category: X, topic: Y` in HISTORY.md |
| User ignores all suggestions | User continues with unrelated topic | Log `[IGNORED] none-selected, user-topic: Z` |
| User consistently selects a category | 3+ selections of same category in last 10 entries | Promote that category tier: MODERATE → STRONG |
| User never selects a category | 0 selections in last 15 entries that included it | Demote that category tier: MODERATE → WEAK |
| User explicitly customizes | Detects customization pattern (see CUSTOMIZATION.md) | Log `[CONFIG-CHANGE] property: X, old: A, new: B` |
| User explicitly disables | "turn off next steps / disable suggestions" | Log `[DISABLED]`, set `enabled: false` |

## Category Preference Learning

### Promotion Rules
- 3+ selections of category X in last 10 history entries → promote X to STRONG
- Category in WEAK tier with 2 selections in last 10 → promote to MODERATE

### Demotion Rules
- 0 selections of category X in last 15 entries where X was presented → demote X one tier
- Minimum tier is WEAK (never fully drop a category)

### Slot Reallocation
When promotions/demotions occur, recalculate slot allocation:
1. STRONG categories get guaranteed slots
2. MODERATE categories share remaining slots via round-robin
3. WEAK categories fill in only when spare slots exist
4. If STRONG slots exceed display-count, rotate STRONG categories

See CATEGORIES.md for the full slot allocation algorithm.

## Implicit Count Learning

Track the display-count the user actually engages with:

1. If user selects suggestion N (where N > current display-count setting), increase count
2. If user consistently selects only from top 3 (for 5+ interactions), log hypothesis: "user prefers fewer suggestions"
3. After 5 consistent observations, adjust `learned-display-count`

Confidence levels:
- **LOW**: < 5 observations supporting the hypothesis
- **MEDIUM**: 5-9 consistent observations
- **HIGH**: 10+ consistent observations

Only auto-adjust display count when confidence is HIGH. At MEDIUM, mention it as a suggestion ("I notice you usually pick from the first 3 — want me to show fewer?").

## Hypothesis Tracking

Format for HISTORY.md entries:

```
[HYPOTHESIS] id: H1, statement: "user prefers deep-dive suggestions", evidence: 4/10 selections were deep-dive, confidence: MEDIUM
[EXPERIMENT] id: H1, action: promoted deep-dive slots by 1 for next 5 interactions
[VALIDATED] id: H1, result: selection rate increased from 40% to 60%, confidence: HIGH → applied permanently
```

Rules:
- Maximum 3 active hypotheses at a time
- Each hypothesis must have at least 3 data points before creating
- Experiments run for exactly 5 interactions
- If experiment shows no improvement or negative result, revert and mark hypothesis as REJECTED

## Self-Diagnostic

Trigger a self-diagnostic after every 20 HISTORY.md entries:

### Diagnostic Procedure
1. Count total selections vs total presentations
2. Calculate per-category selection rates
3. Identify categories with 0% selection rate
4. Identify topics that appear in "user-topic" of IGNORED entries but never in suggestions
5. Review active hypotheses — any stale (> 30 entries old)?
6. Check for patterns in ignored suggestions

### Diagnostic Actions
- Log `[DIAGNOSTIC] overall-rate: X%, best-category: Y (Z%), worst-category: W (V%), gaps: [list]`
- Demote categories with < 10% selection rate over diagnostic period
- Add topics from gap analysis to Topic Affinities as MODERATE
- Close stale hypotheses as INCONCLUSIVE

## History Overflow Management

When HISTORY.md exceeds 50 entries:
1. Take the oldest 25 entries
2. Summarize them into a single `[SUMMARY]` block:
   ```
   [SUMMARY] period: DATE1-DATE2, entries: 25, selections: 12(48%), top-category: deep-dive(5), promotions: 1, demotions: 0, hypotheses-tested: 1(validated)
   ```
3. Delete the 25 individual entries
4. Keep the summary + the newest 25 entries

## Backlog Maintenance

When a topic is mentioned in conversation but not acted on:
- Add to BACKLOG.md as `OPEN`
- When user works on a backlog item → mark `IN-PROGRESS`
- When completed → mark `DONE`
- When user explicitly dismisses → mark `DISMISSED`

Include 1 backlog item in next steps when `include-backlog: true` (default) and there are OPEN items.

When BACKLOG.md exceeds 30 active items (OPEN + IN-PROGRESS), archive DONE/DISMISSED items older than 30 interactions.
