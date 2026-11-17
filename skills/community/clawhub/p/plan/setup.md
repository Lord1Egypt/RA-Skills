# Setup — Plan

Read this on first use to load planning state. Do not interview the user.

## Your Attitude

Planning is a risk decision, not ceremony. Plan exactly as much as the task deserves — no L4 theater on trivial work, no cowboy one-shots on migrations. The human should feel that your plans exist to protect their time and their data, not to perform diligence.

## Data Layout

```
~/Clawic/data/plan/
├── config.yaml     # Configuration variables (table in SKILL.md)
├── outcomes.md     # Current Defaults block + append-only outcome records (format in outcomes.md)
└── active/         # live plan files for multi-session work (long-horizon.md)
```

Empty or missing files = early stage, not a defect: execute, record, learn.

## How To Load State

1. Read `~/Clawic/data/plan/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults from the Configuration table in `SKILL.md` — do not ask.
   - `quick_task_minutes: 30`, `plan_artifact: chat`, `always_validate: [migration/*, external-send/*]`, `stale_after_days: 7`.
3. Read the Current Defaults block of `~/Clawic/data/plan/outcomes.md` for per-type plan levels, strategies, and validation status. Absence is fine; proceed with the depth table.
4. Check `active/` for a live plan before starting new work on the same goal (`long-horizon.md`, Resume Protocol).

Work from defaults immediately. Never open with questions about how much planning the user wants.

## Recording Preferences (only when the user declares one)

Write to config or the defaults block **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a threshold, artifact preference, or a type that must always be validated → update the matching key in `config.yaml`.
- User waives validation, trims plans, or asks for deeper plans on a type → adjust that type's line in the Current Defaults block of `outcomes.md` (Learning Loop rules in `SKILL.md` still gate auto-execute).
- User corrects your depth choice → record which signal you misread, adjust the type default.

If the user has said nothing, store nothing.
