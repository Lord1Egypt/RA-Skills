# mc Operations Playbook

Use these workflows to run MinIO tasks with clear preflight and verification steps.

## Baseline Preflight

Before any write action:
- verify alias target and environment
- capture current state for buckets and policies
- confirm approval for mutating scope

Suggested read commands:
- `mc admin info <alias>`
- `mc ls <alias>`
- `mc policy ls <alias>`

## Bucket Lifecycle Workflow

1. Inspect current bucket settings.
2. Confirm versioning and retention requirements.
3. Apply changes in smallest safe scope.
4. Validate with independent read checks.
5. Record change and timestamp in `incidents.md` or `buckets.md`.

## Identity and Policy Workflow

1. List users, groups, and attached policies.
2. Diff requested policy against effective policy.
3. Apply least-privilege policy update.
4. Re-test access with representative operations.
5. Rotate credentials if scope changed materially.

## Replication Workflow

1. Verify source and target versioning state.
2. Validate clock sync and endpoint reachability.
3. Configure replication rule.
4. Test object flow on controlled prefix.
5. Review lag and failed events before expansion.

## Verification Checklist

After each mutating action, confirm:
- expected policy behavior from a scoped test
- expected bucket settings from direct read commands
- no new errors in admin status output
- rollback path is still valid

If any check fails, treat the change as incomplete and recover before continuing.
