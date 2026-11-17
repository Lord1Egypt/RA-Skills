# Log Template — Data Formats

All files live in `~/Clawic/data/period/`. Three files, three jobs: `config.yaml` = declared, `cycles.md` = the data, `memory.md` = observed.

## cycles.md — the canonical log

```markdown
# Cycle Log

## Cycle 14
start: 2026-03-27          # Day 1 = first day of full flow (never spotting)
end: 2026-04-01            # last bleeding day
length: 29                 # this Day 1 to next Day 1; fill in when the next cycle starts
flow: [d1 medium, d2 heavy, d3 medium, d4 light, d5 light, d6 spotting]   # her scale
symptoms:
  - d1 cramps moderate (ibuprofen helped)
  - d2 headache mild
  - d25 mood-low mild
notes: travel days 8-12
fertility:                 # ONLY when fertility_tracking is not off
  - d13 opk positive
  - d15 bbt-shift confirmed
```

Rules:
- One `## Cycle N` block per cycle, newest last. `length` stays blank until the next Day 1 lands — never estimate it.
- Symptom lines: cycle day, symptom, severity (mild/moderate/severe as defined in `symptoms.md`), optional note in parentheses.
- Off-method bleeds on hormonal contraception: log the same way but tag the block `method: <name>` — these blocks are excluded from prediction math (`contraception.md`).
- An EC dose, illness, or other disruptor goes in `notes` — it explains an outlier later without excluding the cycle.
- Never delete or rewrite past entries except on her deletion request (`privacy.md`).

## config.yaml — what she declared

```yaml
fertility_tracking: off        # off | conceive | avoid
contraception: none            # method name or none
prediction_window: 6           # 3-6 cycles feeding the median
temperature_unit: celsius      # celsius | fahrenheit
heads_up_days: 0               # 0 = only on request
preferences:
  wording: plain               # plain | clinical | her exact phrasing choices
  flow_scale: light-medium-heavy
  proactivity: on-request      # on-request | surface-patterns
  off_limits: []               # e.g. [fertility, weight]
```

## memory.md — what the agent observed

```markdown
# Period Memory

## Status
status: ongoing                # ongoing = baseline forming | established = >=3 cycles logged
last: YYYY-MM-DD

## Baseline (recompute every new cycle)
median_length: 28
spread: 26-34                  # shortest-longest in the prediction window
half_spread: 4                 # rounds up; the ± on every prediction
typical_duration: 5
typical_flow: medium

## Patterns Worth Watching
<!-- e.g. "headache d1-d2 in 4 of last 5 cycles" — surface per proactivity preference -->

## Context
<!-- life-stage notes she has shared: postpartum, perimenopause markers, method changes -->

---
*Updated: YYYY-MM-DD*
```

Baseline math comes from SKILL.md rules 2-3; prediction uses the last `prediction_window` cycles and never cycles older than 12 months — storage keeps everything, the estimate does not.
