# OBD Trace Evidence

Use this workflow to retrieve and interpret an OBD trace ID. A trace is correlated log evidence; it is not itself a task with a success state.

## Fix the Evidence Boundary

Before retrieval, record the controller host and user, exact OBD executable/build, resolved `OBD_HOME` and whether it was originally unset or explicit, originating command, deployment or other target, trace ID, and approximate start/end time. Resolve the home through the shared operation contract rather than assigning a guessed metadata path. Retrieve the trace under the same controller identity and unchanged environment that produced it. A trace from another user, installation, or home directory is not interchangeable evidence.

Read the installed help first. When supported, the public command shape is:

```bash
obd display-trace <trace_id>
```

Do not invent a deployment operand, log-directory option, or timeout flag.

## Interpret the Result

The inspected 4.7 development implementation validates only that the operand is a UUID version 1, greps the local OBD log directory, prints stdout, and returns success without checking the grep exit code, stderr, or whether any line matched. Therefore:

- command exit zero does not prove that the trace exists;
- empty output is `not found/unknown`, not a successful trace check;
- non-empty output must match the originating command, target, controller identity, and time window before it can be attributed to this operation;
- log lines and an apparent terminal message remain evidence to corroborate with the registered state and domain-specific runtime or data-plane checks.

If output is empty or attribution is ambiguous, preserve that result and stop using the trace as proof. A direct read of the resolved local log files is a separate controller read: perform it only when authorized, retain the exact path and permissions, and apply the same non-empty and attribution checks. Do not switch `OBD_HOME`, broaden a filesystem search, or use another user's logs merely to find a matching ID.

## Sensitive and Failed Traces

Trace content can contain commands, paths, SQL, component errors, or credentials exposed by an affected workflow. Keep raw evidence access-controlled, redact secret values in reports, and preserve the non-secret identity and ordering needed to diagnose the operation. Do not delete or rewrite a trace to remove a secret; handle the exposed credential separately.

After a failure, timeout, or interruption, use the shared [failure recovery workflow](../../references/failure-recovery-and-evidence.md). Do not retry, clean, or claim a terminal task state from `display-trace` output alone.

For unattended or multi-stage work, attach the trace ID and attribution result to the structured record defined by [non-interactive automation execution](../../references/automation-execution.md); do not substitute raw trace text for the task, control-plane, runtime, or data-plane event fields.

## Maintainer Evidence

The inspected 4.7 behavior is implemented by `DisplayTraceCommand` in `_cmd.py` and `LocalClient.execute_command` in `ssh.py`. Runtime interpretation must still verify the installed implementation and resolved log location.
