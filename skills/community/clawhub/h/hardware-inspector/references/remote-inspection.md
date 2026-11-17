# Remote inspection

Use remote inspection only when the user explicitly asks to inspect a named SSH host or Kubernetes pod. The runner streams the bundled collector to the target's standard input and executes it as `python3 -`; it does not install the skill or create a remote file.

## Preconditions

The machine running the agent needs:

- OpenSSH `ssh` for an SSH target, or `kubectl` for a Kubernetes pod;
- existing authentication configured for that client;
- network access to the requested target.

The target needs Python 3.9 or newer. Do not install Python, copy credentials, create a pod, or change cluster permissions merely to run the inspection.

## SSH workflow

Preview the exact argument list without connecting:

```bash
python scripts/remote_inspect.py ssh robot@robot.local --dry-run
```

Run the inspection:

```bash
python scripts/remote_inspect.py ssh robot@robot.local --format json
```

Optional supported connection arguments are `--port` and `--identity-file`. The runner:

- preserves normal SSH host-key checking;
- sets `BatchMode=yes`, so password or keyboard-interactive prompts fail instead of blocking or consuming collector input;
- uses the user's existing SSH config, agent, known-hosts file, and identity handling;
- rejects targets shaped like command-line options or shell expressions;
- passes only a fixed, validated remote Python command.

If an existing SSH config requires interactive MFA, perform the authorized login setup outside the runner or use an already authenticated connection mechanism. Never disable host-key checking or expose a private key in output.

## Kubernetes workflow

Specify a pod and, when ambiguity is possible, its namespace and context:

```bash
python scripts/remote_inspect.py kubernetes trainer-0 \
  --namespace ml \
  --context research-h100 \
  --container trainer \
  --format json
```

`k8s` is an alias for `kubernetes`. The runner uses `kubectl exec -i` and the credentials and authorization already selected by `kubectl`. It does not call `kubectl cp`, create resources, or persist the collector.

Before connecting, resolve the exact pod, context, namespace, and container from the user's request or current task context. Do not guess between similarly named production and development contexts. If the user only says “the cluster” and multiple contexts are plausible, ask which target they mean.

The report describes the selected container. Its cgroup limits and visible GPUs/MIG instances are stronger evidence for usable resources than the physical node inventory. Kubernetes requests are normally not visible from inside the pod.

## Collector options

Options after the transport target configure the remote collector:

- `--format json|markdown` selects output; JSON is the default for agents.
- `--full` adds slower peripheral, ROCm-agent, and ML-framework probes.
- `--probe-timeout SECONDS` bounds each normal remote command.
- `--transport-timeout SECONDS` bounds the entire SSH or Kubernetes operation.
- `--python COMMAND` selects a validated Python executable such as `/usr/bin/python3`.
- `--output PATH` writes the report to a local file, never the target.
- `--no-redact` disables redaction only when the user explicitly requests it.

Use `--full` only when the additional evidence is needed. Importing installed ML frameworks may initialize accelerator runtimes or briefly consume resources, which can be undesirable in a production workload.

Remote JSON includes a `transport` object recording that a network connection was used, the collector was streamed over stdin, and no target identifier or remote file was added to the report. Markdown receives an equivalent note.

## Failures and boundaries

- Missing `ssh`, `kubectl`, or remote Python is an actionable prerequisite failure, not evidence about the hardware.
- An SSH host-key or authentication error must be surfaced unchanged; do not bypass it.
- A Kubernetes authorization error means the current identity lacks `pods/exec`; do not request broader rights automatically.
- A timeout can cover connection setup or collection. Increase it only when the user expects a slow target.
- The remote collector remains read-only, but the transport itself is a network action and starts a short-lived Python process on the target.
- Transport stderr can contain host, context, namespace, or organization-specific names. Review errors as well as reports before sharing them.
