# Automation Policies and Scheduled Tasks

## Automation Manager overview

Automation Manager (AMP) provides drag-and-drop policy scripting for repeatable maintenance/remediation.

Key constraints and notes:
- Large policies can become slow in Designer; split and compose with Run Policy.
- Policy upload size limits apply.
- Concurrent SSH-object policies can behave unexpectedly.
- AMP-based services require PowerShell 5.x on target devices.
- Backward compatibility depends on object versions supported by agent.

## Running automation policies in N-central

Policies can be executed via:
- **Scheduled task** (one-time/recurring),
- **Rule-driven scheduled task profiles**,
- **On-demand task execution from device tools**.

## Add automation policy task (high-level flow)

1. Go to Scheduled Tasks and create Automation Policy task.
2. Set task metadata and optional update behavior.
3. Select execution security context (system/current user/custom credentials).
4. Choose policy from repository.
5. Map input/output parameters (including custom properties).
6. Select targets (explicit devices or filter snapshot).
7. Configure schedule and offline behavior.
8. Configure notifications for success/failure.
9. Save and verify first run results.

## Dual-list selector buttons (targeting and similar fields)

Many N-central dialogs use a two-list selector: available items on the left, selected items on the right.

- `>`: move highlighted item(s) from left to right (add selected).
- `>>`: move all currently listed items from left to right (add all visible).
- `<`: move highlighted item(s) from right to left (remove selected).
- `<<`: move all currently listed items from right to left (remove all visible).

Operational notes:
- The right-side list is the effective target set at save time.
- Search/scope filters change what "all" means for `>>` and `<<`.
- For safer changes, prefer `>`/`<` with an intentional shortlist over `>>`/`<<`.

## Critical targeting behavior: filter snapshots

When using filters in tasks, N-central captures a **snapshot** of matching devices at creation/run context, not a continuously live dynamic set. For continuously applied behavior, prefer scheduled task profiles associated via rules.

## Execution context caveats

- Custom credentials use thread-level impersonation (not full session).
- Some environment variables/network behavior may differ vs interactive user session.
- If task needs user context (printers/profile/session interactions), choose current-user execution mode where appropriate.

## Offline and timing behavior

- Configure offline action window and post-power-on delay.
- For recurring tasks, avoid overlap with next recurrence.
- Tasks run in target device timezone; server/device timezone differences can affect interpretation.

## Common scheduled task types in operations

- Automation policy tasks
- AV/Security scans (full/quick/custom)
- File transfer tasks
- Backup/export tasks
- Script tasks (Windows/macOS)
- Restart service tasks
- Third-party software push

## Probe/agent interaction notes

- Some tasks can run via agent and/or probe.
- Probe-based profiles may stop when associated probe changes; re-engage by updating associated rule or probe assignment.

## Custom services from policy outputs

Policies exposing Global Output Parameters can feed custom services for:
- thresholds,
- notifications,
- self-healing,
- reporting.

Use this when policy outcomes should become continuously monitorable service states.

## Troubleshooting failed policy runs

1. Validate policy parameters and property mappings.
2. Confirm device prerequisites (.NET, PowerShell, required modules/objects).
3. Confirm execution identity has needed rights.
4. Check offline/maintenance window conflicts.
5. Inspect task history and per-device run logs.
6. Re-test on single known-good device before broad rerun.
