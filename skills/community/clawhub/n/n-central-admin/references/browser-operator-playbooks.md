# Browser Operator Playbooks (for AI-assisted administration)

## Session prep

- Confirm correct N-central tenant/environment.
- Confirm role permissions and current scope.
- Open one tab for list views and one for device details comparisons.
- Record target counts before and after changes.

## Reliable navigation pattern

1. Navigate to target module.
2. Wait for filter/search panel to stabilize.
3. Apply one criterion at a time.
4. Re-check resulting counts.
5. Save only when expected count and composition match intent.

## Rule creation playbook

1. Draft/choose filter(s) and preview members.
2. Create rule with explicit name/description.
3. Configure target filters (remember OR behavior across multiple filters).
4. Configure actions (template/task/notification/features).
5. Configure grants/propagation.
6. Save and validate on sampled devices.
7. Audit associations and logs.

## Scheduled task playbook

1. Select task type.
2. Choose execution context.
3. Target devices (prefer pilot first).
4. Configure schedule and offline handling.
5. Configure notifications.
6. Save and monitor first run completion/failure details.

## Device triage playbook

1. Overview for immediate health signals.
2. Monitoring for failing services/associations.
3. Tools for direct remediation.
4. Settings for persistent config fixes.
5. Add note and verify resolved state.

## UI stability patterns

- Prefer explicit waits for list/table refresh before next click.
- Re-snapshot after major navigation.
- Avoid chained clicks when modals/spinners are active.
- If list contents reorder asynchronously, sort before selection.
- For destructive/broad actions, require human confirmation checkpoint.

## Common failure modes and recovery

- **Wrong scope edits**: immediately disable/rollback object and recreate at correct scope.
- **Over-broad filter**: clone + tighten expression; avoid hot-editing production filter in place.
- **Task did not hit expected endpoints**: confirm snapshot timing and offline windows.
- **Rule appears saved but no effect**: force reevaluation with safe update and verify event triggers.

## Audit evidence to capture

- Filter expression and match count.
- Rule/task name, scope, and associated artifacts.
- Timestamp and operator account.
- Validation screenshot or notes from 1–3 sample devices.
