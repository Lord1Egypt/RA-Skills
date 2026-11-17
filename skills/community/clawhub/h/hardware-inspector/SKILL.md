---
name: hardware-inspector
description: Inspect local or explicitly requested remote systems' hardware, drivers, firmware, accelerators, and runtimes with a privacy-safe, read-only report. Stream the collector to SSH hosts or existing Kubernetes pods without remote installation. Use when an agent needs machine specifications, GPU or accelerator details, CUDA/ROCm/Metal readiness, driver versions, CPU/RAM/storage inventory, Raspberry Pi or NVIDIA Jetson identification, thermal or power context, Kubernetes, container, cgroup, Slurm, or virtualization resource limits, or a reproducible profile for compatibility and performance debugging on Linux, macOS, or Windows.
---

# Hardware Inspector

Collect machine facts with the bundled dependency-free Python script, then interpret the evidence for the user's actual question. Treat the report as a snapshot of hardware exposed by the operating system, not proof that every physical component was discovered.

## Inspect the current environment

Resolve `scripts/hardware_report.py` relative to this `SKILL.md`, then run:

```bash
python scripts/hardware_report.py --format markdown
```

For a deeper accelerator and peripheral inventory, run:

```bash
python scripts/hardware_report.py --full --format json --output hardware-report.json
```

Use `--full` only when peripheral or ML-framework readiness matters. It imports installed frameworks and may initialize accelerator runtimes or briefly consume accelerator resources; prefer the default report in production workloads.

Prefer JSON when another tool or agent will consume the report. Prefer Markdown when a human will read it. Do not use `sudo`, install packages, access the network, or change system configuration to obtain more data.

## Inspect an SSH host or Kubernetes pod

Use remote inspection only when the user explicitly asks to connect to a named target. If the agent already runs inside that target, use the local collector instead.

Stream the collector to an SSH host without installing it there:

```bash
python scripts/remote_inspect.py ssh robot@robot.local --format json
```

Stream it into an existing Kubernetes pod:

```bash
python scripts/remote_inspect.py kubernetes trainer-0 --namespace ml --context research-h100 --container trainer --format json
```

Resolve the exact host or pod, context, namespace, and container before connecting. Preserve normal SSH host-key verification and existing `ssh` or `kubectl` authentication. Do not copy credentials, disable verification, create cluster resources, broaden permissions, or install remote dependencies. Read [remote inspection](references/remote-inspection.md) for options, security boundaries, and failure handling.

## Interpret the evidence

1. Answer from successful probes and label unavailable information as unknown.
2. Distinguish hardware presence, kernel or OS driver state, toolkit installation, and framework readiness. These are separate layers.
3. In containers and scheduler jobs, distinguish node capacity from the process allocation. Prefer cgroup CPU and memory limits plus visible accelerator devices when stating what the workload can actually use.
4. Treat the CUDA version shown by `nvidia-smi` as the driver's supported CUDA level, not necessarily the installed CUDA toolkit version. Use `nvcc --version` for the latter.
5. On Jetson, do not treat a missing `nvidia-smi` as a GPU failure. Prefer the board model, L4T release, `tegrastats`, and `nvpmodel` evidence.
6. When commands disagree, show the conflicting values and identify which source is closest to the layer under investigation.
7. Base compatibility or upgrade advice on current official vendor documentation; versions and support matrices change over time.

Read [platform notes](references/platform-notes.md) when diagnosing accelerators, Raspberry Pi, Jetson, containers, or virtualization.

## Present the result

Lead with a compact summary relevant to the request. Include:

- the detected platform and architecture;
- CPU, memory, storage, and accelerators relevant to the task;
- cgroup or scheduler limits and the accelerators visible to the current process when running in Kubernetes, Slurm, or another containerized environment;
- driver, toolkit, and framework versions when compatibility matters;
- missing probes or uncertainty that affects the conclusion;
- concrete next checks only when the existing evidence is insufficient.

Do not paste the entire raw report into chat unless the user asks for it. Do not claim the script inspected devices hidden by firmware, passthrough boundaries, permissions, containers, or unsupported operating-system APIs.

## Preserve privacy and safety

The collector is read-only, invokes commands without a shell, uses timeouts, and makes no network requests. The remote runner uses the network only after an explicit SSH or Kubernetes inspection request and records that transport in the report. Redaction is enabled by default for hostnames, usernames, home paths, serial numbers, UUIDs, MAC addresses, and IP addresses.

Use `--no-redact` only when the user explicitly requests an unredacted report and understands that it may contain identifying data. Review any report before publishing it in an issue, pull request, forum, or chat.
