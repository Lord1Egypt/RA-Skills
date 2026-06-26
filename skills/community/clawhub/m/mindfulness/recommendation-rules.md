# Recommendation Rules - Mindfulness

Use these rules to generate one primary recommendation plus one fallback.

## Decision Inputs

- recent adherence (last 7 days)
- average state shift (post minus pre)
- available time window
- current stress level
- user preference for guidance intensity

## Recommendation Matrix

| Condition | Primary recommendation | Fallback |
|-----------|------------------------|----------|
| low adherence + low time | 1-minute reset anchored to existing routine cue | 3-minute breathing space once daily |
| low adherence + high stress | reset mode twice daily at fixed times | one guided 5-minute body scan at end of day |
| medium adherence + flat outcomes | switch technique for 1 week | keep technique and adjust session timing |
| high adherence + positive outcomes | incremental duration increase (plus 2 minutes) | keep duration and add one reflection prompt |
| high adherence + high stress spikes | add trigger-specific reset protocol | add midday guided session |

## Weekly Adjustment Rule

At weekly review, change only one variable:
- duration
- timing
- technique
- frequency

Do not change more than one variable unless user asks.

## Stop Conditions

- If practice increases distress consistently, pause progression and simplify.
- If user reports crisis-level symptoms, stop this workflow and direct immediate professional support.
