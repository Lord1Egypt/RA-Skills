# Change Control Log Template - Google Workspace CLI

Use this file to record every mutating operation plan and result.

## Entry Template

```markdown
## YYYY-MM-DD HH:MM - Operation
- command_id:
- account:
- tenant:
- mode: dry_run | apply
- command:
- impacted_objects:
- expected_side_effects:
- dry_run_evidence:
- confirmation_token:
- rollback_plan:
- result:
- follow_up_checks:
```

## Minimum Evidence Rules

- Every apply command must have a dry-run or schema evidence record.
- `impacted_objects` must include stable ids, not display names.
- `confirmation_token` must be copied exactly from user approval.
- `result` must include success or failure signal from command output.

## Rollback Notes

Include one practical rollback path for each mutating operation:
- delete/create reversal approach
- permission/share rollback command
- notification or communication rollback where applicable

## Verification Checklist

After apply commands:
- run at least one read-only verification command
- confirm expected state change is visible
- document mismatch in `incidents.md` if verification fails
