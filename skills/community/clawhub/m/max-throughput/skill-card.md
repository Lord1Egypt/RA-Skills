## Description:

Max Throughput helps agents inspect compute resources, parallelize CPU and GPU workloads, and profile bottlenecks to reduce wall-clock time for training, evaluation, benchmarks, preprocessing, builds, and tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promethe-us](https://clawhub.ai/user/promethe-us)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when running compute-heavy jobs or diagnosing slow jobs. It guides the agent to inspect local resources, launch safe parallel work, profile utilization, and tune the measured bottleneck.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggressive parallel execution can exhaust CPU, GPU, RAM, quotas, or shared production capacity.

Mitigation: Review before installing on shared, production, CI, or quota-limited machines, and require user confirmation before launching parallel jobs, bulk downloads, MPS, or commands intended to consume all available CPU/GPU capacity.

Risk: Unpinned package or tool execution can download unexpected code.

Mitigation: Prefer manual installation or pinned package commands, and avoid approving unexpected npx or pip downloads.

Risk: Persistent or global agent instructions can make aggressive throughput behavior apply beyond a single task.

Mitigation: Scope installation and global agent instructions to trusted environments, and review persistent performance defaults before enabling them.

## Reference(s):

- [CPU Parallelism Playbook](references/cpu-parallelism.md)
- [Experiment Packing on Multi-GPU Machines](references/experiment-packing.md)
- [Profiling Playbook: Find the REAL Bottleneck](references/profiling.md)
- [PyTorch Multi-GPU Playbook](references/pytorch.md)
- [Tuning Playbook: Knobs That Actually Help](references/tuning-playbook.md)
- [Agent Skills](https://agentskills.io)
- [skills CLI](https://skills.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and optional JSON from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resource probes can emit human-readable text or JSON; triage scripts report sampled utilization and bottleneck guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
