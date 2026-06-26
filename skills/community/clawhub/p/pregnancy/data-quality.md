# Data Quality Rules - Pregnancy

Use these checks before storing entries or generating summaries.

## Required Fields per Entry

- timestamp
- metric or symptom name
- value with unit (or severity scale)
- context label

If one required field is missing, request clarification before saving.

## Consistency Rules

1. Unit lock
- once a metric is tracked in one unit system, keep it consistent
- if conversion is needed, show both source and normalized value once

2. Context lock
- glucose must include fasting or post-meal context
- blood pressure should include rest state and repeat status
- symptom events should include onset and duration

3. Timeline lock
- no backfilling without explicit "estimated" tag
- preserve event order for triage review

## Summary Readiness Checks

Before producing weekly or visit summaries, confirm:
- at least 4 days of data in the period
- no unresolved unit mismatches
- all red and amber events include action taken
- open clinician questions are listed

## Noise Reduction Rules

- Do not overinterpret single outlier values.
- Prioritize trends and repeated patterns.
- Separate user feelings from measured values while keeping both.
- Keep optional wellness metrics secondary to clinical signals.

## Failure Modes to Avoid

- raw data dump with no trend synthesis
- mixing observation and diagnosis language
- missing escalation note after warning events
- collecting fields the user never uses
