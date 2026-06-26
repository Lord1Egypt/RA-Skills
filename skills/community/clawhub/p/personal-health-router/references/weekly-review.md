# Weekly Health Review (Unified)

Use this branch for cross-domain assessments combining nutrition, exercise, and sleep.

## Scope
- Create a weekly health review from recent signals.
- Identify the main bottleneck and next-step actions.
- Rebuild the `Weekly Health Assessment` table in Feishu.

## Analysis Rules
- Combine signals from all three domains.
- Highlight conflicts (e.g., high training load + poor sleep).
- Provide practical, action-oriented next-week advice.

## Reporting Rules (Feishu)
- Assume the `rebuild_weekly_assessment.py` script handles the heavy aggregation.
- The agent should trigger the script for the target week.
- For a manual text summary, use the `brief` template logic from the script.

## Command Template
```bash
python3 scripts/rebuild_weekly_assessment.py <config.json> \
  --identity user \
  --week-end 2026-05-03 \
  --json
```

## Boundary
For daily trend scanning, use the `Monthly Health Calendar` or the dashboard instead.
