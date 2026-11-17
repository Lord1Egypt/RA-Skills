# Host Environment Initialization

Use `obd cluster init4env` only when a version-supported deployment check identifies a host setting that the installed workflow is designed to initialize. It is a persistent operating-system mutation; stopping, destroying, redeploying, or pruning the deployment does not roll it back.

Do not use it to bypass port conflicts, occupied/overlapping paths, incompatible packages, architecture/runtime mismatches, cgroup or CPU-affinity constraints, insufficient resources, network failures, or unknown processes.

## Capability and Diff Gate

1. Record the OBD build, `cluster init4env --help`, deployment/configuration, selected plugins, targets, SSH identity, and current status.
2. Reproduce the relevant environment/strict check and preserve trace/evidence. Map each finding to a specific setting supported by the installed init workflow.
3. Inspect the installed workflow and capture every live value, persistent file, service/unit, account, ownership, or permission it can change.
4. Produce a per-host diff: current value, intended value, persistent location, runtime/reboot effect, exact rollback, and any reconnect/reboot requirement.
5. Detect duplicate or conflicting entries and other automation that owns those settings. Stop when the intended final value or owner is ambiguous.

Do not invent a dry-run option. A verified OBD 4.7.x surface does not expose one, so derive the diff from version-matched implementation evidence before executing. If the exact persistent changes cannot be identified, stop and report that host initialization cannot be bounded.

When `init4env` is a necessary, version-supported step of the user's requested execution, the request already authorizes its exact reviewed per-host persistent diff. Record the targets, effects, and rollback, but do not ask for a second confirmation merely because the changes persist. Optional or broader host changes remain out of scope.

## Execute and Verify

Use the installed syntax, commonly:

```bash
obd cluster init4env <deploy_name>
```

The reviewed command has no public confirmation option, while its workflow can display a system-parameter change list and prompt before applying it. When execution is unattended and the check can produce a non-empty change list, launch the **first and only invocation through a real PTY from process start**. Do not probe with redirected stdin or a non-TTY invocation first and retry only after it fails. Use the command-specific procedure in [non-interactive automation execution](../../references/automation-execution.md); pipes, here-documents, `yes`, and input written to a process without a controlling PTY are invalid.

Before launch, record the installed build's exact no-change terminal message, change-list marker, and confirmation prompt. The PTY driver must:

1. start only `obd cluster init4env <deploy_name>` for the already resolved deployment and capture its PID and redacted transcript;
2. accept a terminal no-change result without sending input, or wait until the complete per-host change list and the exact expected confirmation prompt have both appeared;
3. compare the displayed deployment identity and every displayed setting/value with the reviewed diff, then send exactly one affirmative response followed by Enter;
4. send nothing on an unexpected, repeated, truncated, or differently scoped prompt, keep the PTY attached until the command reaches a terminal exit, and reconcile the trace and host state before any retry.

A missing or incorrectly allocated PTY is an automation defect, not evidence that `init4env` is unsupported. Correct the driver only after proving the failed invocation is terminal and made no mutation; it does not authorize a manual sysctl/limits workaround.

Prefer the supported `init4env` path. A manual equivalent is allowed only when all of the following are proved:

1. the exact installed `init4env` workflow is version-supported but remains unusable after a correctly allocated, prompt-matched real-PTY invocation; absence or misconfiguration of that PTY does not satisfy this condition;
2. the failed invocation is terminal and evidence proves whether it changed anything;
3. the workflow's complete per-host change list, target values, persistent files, live effects, and rollback are known, and every item is necessary to clear the original deployment check;
4. the manual plan applies exactly that bounded diff under the same target identity, without extra tuning, duplicate entries, broader limits/sysctl changes, or a reboot.

The original request authorizes this exact necessary equivalent diff under the same persistent-change rule; do not ask for a duplicate confirmation. If the equivalence or prior state cannot be proved, stop rather than improvising host tuning.

Preserve the trace and the exact execution path. On every target verify live and persistent values, ownership/permissions, expected boot behavior, absence of duplicate/unrelated changes, and the original failed check. For PAM limits or another setting applied at login/session creation, open a fresh SSH login under the actual deployment user and verify `ulimit` there; a pre-existing shell retaining the old value is not failure evidence. If the installed workflow says a reboot may be required, report that pending effect and do not reboot unless the user requested it. A successful exit is insufficient.

If a host is partially changed, freeze cluster retries. Before rollback, re-inventory every deployment, process, and organization-owned baseline that may now depend on the changed host settings. Complete only the original exact diff, or treat a reviewed itemized rollback as a new recovery action after proving that it will not break those dependencies. Do not broaden sysctl/limits edits, force the workflow, or redeploy.

Track host changes separately from deployment metadata. Deployment removal must not trigger automatic host rollback. When the deployment is later removed, report retained settings and re-inventory current dependants. Apply a rollback only when the user requests that separate recovery outcome; do not infer it from deployment removal.
