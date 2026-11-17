# Non-Interactive Automation Execution

Use this workflow for unattended or multi-stage OBD automation. It supplements the [operation contract](operation-contract.md); it does not authorize a mutation, package installation, credential exposure, or a broader target.

## Preflight the Runner

Before the first OBD, SSH, SQL, or helper invocation, record and verify:

- the automation runner, selected controller, artifact-acquisition host, managed hosts, user and SSH hop for each, working directory, shell, and non-secret environment; for remote workflows, confirm that OBD execution and metadata remain on the remote controller unless the user explicitly selected otherwise;
- the exact controller-side `obd` executable/build and resolved controller home;
- whether `OBD_HOME` was originally unset or explicitly configured, and which registered deployments and traces prove that the resolved controller is the intended one;
- whether stdin is attached to a controllable TTY, which steps can prompt, and how each supported prompt will be handled;
- the exact SQL client or OBD database helper, endpoint mode, and protected credential source;
- every external interpreter and module required by an auxiliary script under the exact executable that will run it;
- the installed public helper/action inventory and the spelling, target scope, interaction mode, and exit behavior of every selected action;
- caller-side and OBD-native timeouts, process ownership, and the state checks that follow either timeout.

Do not assume that OBD's private Python environment, the system Python, or an automation runner contains `mysql.connector` or another client module. Test the required import with the exact interpreter before starting the workflow, or use an already available, supported SQL client. Missing runtime support does not authorize package installation, modification of OBD, or switching to an unrelated interpreter.

Validate helper and action names through the installed public inventory or help first. Inspect a packaged helper template only when the public surface cannot establish a critical name or side effect. Do not invoke a guessed action merely to see whether it exists.

## Handle Confirmation Without Expanding Semantics

For each potentially prompting command, determine before launch whether the installed build provides a command-local, public confirmation option whose only reviewed effect is acknowledging that exact prompt. Use it only after the target, impact, and required authorization have passed their normal gates.

Do not use a controller-wide automatic-confirm setting, generic `yes` input, an unrelated `--force` option, or hidden input to make a workflow unattended. Some command-local options named `--confirm` also trigger restarts or other work; their exact installed semantics still control. If no safe command-local form exists and the command must be answered interactively, use a real PTY with controllable stdin rather than an ordinary pipe, or stop before launching the command.

Immediately before confirmation, display the deployment, component, repository object, or fully expanded deletion set named by the prompt and compare it with the authorized inventory. A confirmation session must acknowledge only that unique named object or exact enumerated set; do not reuse one session or response across adjacent objects.

If an automation client has already left an OBD process waiting for input, identify the caller-owned PID and children, determine whether any mutation began, interrupt only that invocation through its normal caller/session boundary, and reconcile controller and target state before another attempt. Retry only after the first invocation is terminal or absent and idempotence is proved. Never leave an unidentified prompt-waiting process attached to the controller.

### Known OBD Command Interaction Forms

Resolve these forms against the installed help before launch; they are command-specific and must not be generalized to another subcommand:

| Command/path | Unattended handling |
|---|---|
| `cluster destroy` | After the exact destructive target and removal set have already been authorized, reviewed V4.6.0 builds use `--confirm` to acknowledge that one destroy prompt. `-f`/`--force-kill` is process killing, not confirmation, and must never be substituted. |
| `cluster prune-config` | After the exact metadata removal has been authorized, reviewed builds use `--confirm` for that one prompt. It does not authorize destroy or repository cleanup. |
| `cluster init4env` | The reviewed public command has no confirmation option. For unattended execution, allocate a real controlling PTY before the first invocation; never try redirected stdin first. Accept the installed no-change terminal path without input, or wait for the complete per-host change list and exact confirmation prompt, compare both with the reviewed deployment/diff, send one affirmative response plus Enter, and remain attached through terminal exit. Pipes, here-documents, `yes`, and a process without a controlling PTY are invalid. |
| `cluster upgrade` | The reviewed implementation can always display the selected package path and ask for confirmation about a non-official release, with no public bypass flag. Use a real PTY only after the exact hop/package table and upgrade scope pass the upgrade workflow. Do not pipe `yes`, use force, or ask the user for a duplicate confirmation when the explicit upgrade request already covers the proved package transition. |
| `cluster edit-config` | Default to the real-PTY editor path in the [configuration-change workflow](../cluster-management/references/configuration-changes.md#auditable-editing). The editor must rewrite OBD's generated file in place without changing its device/inode; `sed -i`, `perl -pi`, rename, and temporary-file replacement are invalid. Non-TTY complete-YAML stdin is not a portable fallback: use it only when that exact installed build has already been runtime-proved to accept the complete protected document. Reviewed source that contains such a branch does not prove the installed frozen executable does. |
| `mirror clean` and other prompting repository deletion | Use a PTY unless the exact installed command exposes a reviewed confirmation selector. Expand and authorize the exact hash/path set first. |

A PTY driver must wait for and match the expected command-specific prompt before sending its single response, capture a redacted transcript and PID, and fail closed on an unexpected prompt or target. It must not become a generic automatic-answer wrapper.

For an existing deployment whose complete replacement YAML and semantic diff have already been reviewed, prefer the bundled [`obd-edit-config-pty.py`](../cluster-management/scripts/obd-edit-config-pty.py) helper over inventing an `expect` expression. Supply the exact absolute Python interpreter and OBD executable established by the executable-identity preflight plus the reviewed OBD SHA-256; do not launch either through a PATH-resolved bare name. The helper allocates a controlling PTY, uses a same-inode editor, validates the reviewed replacement and OBD checksums, and sends no answers. Any OBD confirmation prompt is therefore a terminal stop for that invocation, not an invitation to broaden the helper.

## Remote Result Envelope for Hanging SSH Sessions

For a long non-interactive OBD command known to complete remotely while its original SSH channel can remain open, do not use that channel's closure as the only completion signal. Run only the already reviewed command inside a unique controller-local directory owned by the current controller user, with mode `0700`, and use a remote result envelope:

1. record the exact command, start time, wrapper PID, expected target, and redacted input checksum;
2. redirect the command's stdin from `/dev/null` only after proving it cannot prompt, and redirect stdout/stderr to permission-controlled files so no child inherits the SSH channel;
3. after the OBD process exits, write its numeric exit code and end time to a temporary status file and atomically rename that file to the final completion marker;
4. poll the marker, wrapper PID, OBD child PID, trace, and target state through fresh bounded SSH connections;
5. accept completion only when the marker and the applicable control-plane, runtime, and data-plane evidence agree.

Do not apply this pattern to `edit-config`, `init4env`, upgrade confirmation, or another command that requires a controlling PTY. A lost polling connection does not authorize a duplicate invocation. If the completion marker never appears, classify the original operation through the shared timeout-reconciliation workflow rather than manufacturing an exit code or deleting the run directory. Remove only this invocation's result-envelope directory after its evidence has been retained or the user-authorized cleanup boundary permits it.

## Record Structured Events

For unattended or multi-stage work, write an append-only JSON Lines record in an approved, permission-controlled local path. Use one event per line and keep raw secrets out of every field. At minimum record:

```text
run_id, operation_id, phase, event, wall_time_utc, monotonic_time,
runner, controller, artifact_acquisition_host, mirror_source_priority,
mirror_source, source_attempt, attempted_route, target,
redacted_command, command_pid, target_pids,
listeners, obd_state, data_plane_probe, trace_or_task_id, result
```

Also record the input/configuration checksum, effective artifact base URL, component/version/release/suffix/architecture, artifact checksum, relevant proxy/repository state, stdout/stderr artifact paths, exit code or caller timeout, selected and unselected objects, and the final removed/retained object sets when relevant. For a package-source retry, keep the operation identity tied to the same exact acquisition and increment `source_attempt` from 1 through 3; changing a proxy route does not change `mirror_source`. Use a stable run ID across the lifecycle and a distinct operation ID per command. Wall-clock timestamps support correlation; monotonic timestamps support duration calculation.

For measured stop, start, or restart availability, capture separate events for the last successful authenticated data-plane probe, listener loss, expected PID transition, listener recovery, and first successful authenticated probe. Command start/end time alone is not database downtime.

## Reconcile the End State

After every invocation, close or account for the local command process, SSH session, helper wrapper, and child task. A caller timeout or disconnected terminal does not prove that OBD or the server-side task stopped. Follow the shared [failure-recovery workflow](failure-recovery-and-evidence.md), append the reconciled terminal or unknown state, and do not submit a duplicate operation while the first invocation remains unresolved.
