# Safety Checklist - Google Workspace CLI

Run this checklist before any command that sends, shares, updates, or deletes data.

## Preflight

- Confirm account and tenant are correct.
- Confirm method schema and required fields.
- Confirm target identifiers are immutable ids, not names.
- Confirm API is enabled for the project.

## Dry-Run Gate

- Run with `--dry-run` when method supports safe preview.
- Record exact command and expected side effects.
- Validate object count and scope boundaries.

## Approval Gate

- Request explicit confirmation token from user.
- Restate affected resources and side effects.
- Block execution if any identifier is ambiguous.

## Apply Gate

- Execute the approved command only once.
- Capture output and save response summary.
- Log rollback path if the operation is reversible.

## Post-Run

- Verify resulting state with read-only commands.
- Update `change-control.md` with evidence.
- Add incident note if output deviates from expected result.
