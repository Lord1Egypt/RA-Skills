# OBD Runtime Environment

Use this reference only when the user explicitly asks to inspect or change `obd env`, developer mode, lock behavior, transfer behavior, or telemetry, or when concrete failure evidence identifies one of them as the cause. It is not a default preflight or test checklist for ordinary deployment and lifecycle work.

Treat `obd env` values and developer mode as persistent controller-wide policy. They can change later commands for every deployment and user of the same OBD home. Read-only inspection should stay limited to the setting relevant to the request or diagnosis.

## Baseline and Concurrency Gate

Before a change, record the controller, user, executable/build, resolved `OBD_HOME`, whether that variable was originally unset or explicit, active CLI/Web/API tasks, developer-mode state, and the installed version's complete OBD environment view. Determine the storage scope and which processes read values only at startup.

Resolve the controller home under the unchanged caller environment through the shared operation contract. Do not export an observed metadata directory as `OBD_HOME`; a value such as `/root/.obd` can be interpreted as a base and produce an unintended `/root/.obd/.obd`. If a scoped operation requires an explicit override, verify the resulting registration and trace location before continuing and restore the original unset/value state afterward.

If another task depends on a value or the baseline cannot be read, do not mutate it. Prefer a command-local option when the installed build provides an equivalent.

## Change One Policy at a Time

- `obd env` subcommands can be hidden from ordinary help in some builds. Prove the exact command and value semantics from the installed build or version-matched documentation before invoking it; do not enable developer mode merely to discover or expose unrelated commands.
- Use exact set or unset operations for the required key. Never use environment clear as cleanup.
- Automatic confirmation can suppress destructive prompts for unrelated later commands. Do not enable it as a benchmark or automation prerequisite, and never treat it as user authorization. If temporarily approved, restore its exact prior state immediately after the scoped command.
- Developer mode can expose hidden commands, accept undefined options, or weaken validation. Enable it only for an explicit development workflow with a reviewed reason and stop condition; restore it afterward.
- Lock-mode changes can weaken controller concurrency protection. Do not downgrade or disable locks to bypass an active task or lock error.
- Transfer, repository-install, SSH-algorithm, base-directory, and Web-idle settings can change persistent paths, security, or runtime behavior. Review the installed meaning and consumers before changing one.
- `OBD_HOME` is part of controller identity, not a convenience switch for finding state. Never change it to make a deployment or trace appear, and do not treat a new empty home as repair.

Do not guess an environment key or value from another OBD version. Save whether the key was absent as well as its value so restoration can distinguish `unset` from a configured default.

## Transfer-Mode Verification

A transfer-related environment value and a log line selecting rsync or SFTP prove only control-path selection. When the user asks to validate transfer behavior, use a disposable, uniquely named file on authorized hosts, perform one real transfer through each requested mode, compare source and destination hashes, and remove only that test artifact. If no real transfer is performed, report the result as PARTIAL rather than PASS. Do not deploy or mutate a component merely to manufacture transfer evidence.

## Telemetry

Before work in an offline, regulated, or sensitive environment, inspect the installed build's telemetry submission and local telemetry logging behavior. Record the current organizational policy, configured values, local log path, and operations that can attempt submission.

Preserve the existing policy by default. Change telemetry submission, logging, or reporter settings only when the user or organization requires it. Submission and local logging are independent; disabling one does not prove the other is disabled. When no-egress behavior matters, verify it under the environment's approved network controls.

Redact deployment names, addresses, usernames, paths, command parameters, and business data before sharing telemetry artifacts. A telemetry failure does not by itself mean the requested OBD operation failed, and telemetry success does not prove it succeeded.

## Restore and Accept

After the scoped operation, restore every temporary key and developer/lock setting to the recorded baseline, including removal of keys that were originally absent. Compare the final environment with the baseline and report intentional persistent differences. Verify that no unrelated active task or deployment changed because of the temporary policy.
