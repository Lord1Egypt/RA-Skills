## Description:

Performance Mastery helps agents diagnose and tune Linux system, container, Kubernetes, and application performance across CPU, memory, disk I/O, networking, kernel parameters, compiler optimization, eBPF tracing, benchmarking, and major programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[husttsq](https://clawhub.ai/user/husttsq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, platform engineers, and performance engineers use this skill to collect baselines, interpret performance tool output, identify bottlenecks, propose tuning changes, and validate changes with benchmark comparisons. It is suited to Linux hosts, containers, Kubernetes workloads, and applications written in Python, Go, Java, Rust, C/C++, or Node.js.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrator-level tuning commands can permanently alter Linux host behavior or reduce service stability.

Mitigation: Begin with read-only diagnostics, test one change at a time outside production, record original values, and keep rollback commands ready.

Risk: Persistent changes to /etc, systemctl, udev, cron, fstab, or sysctl configuration can survive restarts and be hard to unwind during incidents.

Mitigation: Avoid persistent configuration changes on production hosts without backups, a reviewed change plan, and a tested rollback path.

Risk: Benchmark and load-generation examples such as fio, sysbench, iperf3, and wrk can stress systems or affect shared environments.

Mitigation: Run benchmarks against isolated test targets or agreed maintenance windows, and bound duration, concurrency, and data paths.

Risk: Downloaded or external profiling tools can introduce supply-chain risk.

Mitigation: Pin versions and verify downloads before installing or running profiling tools.

## Reference(s):

- [CPU Tuning Reference](references/cpu.md)
- [Memory Tuning Reference](references/memory.md)
- [Disk I/O Tuning Reference](references/disk_io.md)
- [Network Tuning Reference](references/network.md)
- [Kernel Parameter Quick Reference](references/kernel_params.md)
- [Container and Kubernetes Performance Tuning](references/container_k8s.md)
- [eBPF, bpftrace, and BCC Advanced Tracing](references/ebpf_bpftrace.md)
- [Benchmarking Toolkit](references/benchmarking.md)
- [Compiler Optimization Reference](references/compile_optimization.md)
- [Performance Tool Output Guide](references/tool_output_guide.md)
- [Linux Performance Case Studies](references/case_studies.md)
- [Python Performance Guide](references/python_performance.md)
- [Go Performance Guide](references/go_performance.md)
- [Java Performance Guide](references/java_performance.md)
- [Rust Performance Guide](references/rust_performance.md)
- [C/C++ Performance Guide](references/c_cpp_performance.md)
- [Node.js Performance Guide](references/nodejs_performance.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with diagnostic explanations, report tables, and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose administrator-level Linux tuning commands and validation or rollback steps; review commands before execution.]

## Skill Version(s):

3.8.1 (source: ClawHub release metadata; artifact frontmatter says 3.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
