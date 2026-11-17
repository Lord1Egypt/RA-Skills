## Description:

Linux Performance Analyzer helps agents diagnose and tune Linux CPU, memory, disk I/O, network, kernel parameter, compiler optimization, and container/Kubernetes performance issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[husttsq](https://clawhub.ai/user/husttsq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and Linux administrators use this skill to collect Linux performance snapshots, interpret system metrics, identify bottlenecks, and produce tuning plans with validation and rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad root-level or persistent Linux system changes.

Mitigation: Require explicit administrator approval before any root or persistent command, test changes outside production first, and record original values for rollback.

Risk: Performance snapshots and heap-dump outputs may contain sensitive system, process, or application data.

Mitigation: Treat collected outputs as sensitive, limit sharing and retention, and redact secrets or host-specific details before external review.

Risk: Changes touching /etc, systemd, crontab, /proc, or /sys can affect system stability.

Mitigation: Review each proposed change before execution and prefer read-only diagnostics until the target system, workload, and rollback path are clear.

## Reference(s):

- [CPU tuning reference](references/cpu.md)
- [Memory tuning reference](references/memory.md)
- [Disk I/O tuning reference](references/disk_io.md)
- [Network tuning reference](references/network.md)
- [Kernel parameter reference](references/kernel_params.md)
- [Compiler optimization reference](references/compile_optimization.md)
- [Linux performance case studies](references/case_studies.md)
- [Linux Performance](http://www.brendangregg.com/linuxperf.html)
- [perf Examples](http://www.brendangregg.com/perf.html)
- [Linux TCP Tuning](https://fasterdata.es.net/host-tuning/linux/)
- [sysctl Explorer](https://sysctl-explorer.net/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and structured analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed Linux tuning commands, configuration changes, verification checks, and rollback commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
