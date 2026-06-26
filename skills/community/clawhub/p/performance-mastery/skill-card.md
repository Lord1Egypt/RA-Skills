## Description: <br>
Performance Mastery helps agents diagnose and tune Linux, container, and application performance across CPU, memory, disk, network, kernel, compiler, and language runtimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[husttsq](https://clawhub.ai/user/husttsq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and performance engineers use this skill to investigate system slowdowns, resource bottlenecks, runtime hotspots, benchmark regressions, and tuning options before applying measured changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest privileged Linux performance changes that persist across reboots or affect the whole system. <br>
Mitigation: Review every /etc, /sys, /proc, systemd, udev, fstab, and sysctl change before running it; record current values and prepare rollback steps. <br>
Risk: Copy-paste diagnostic or tuning commands may be unsafe as defaults for production systems. <br>
Mitigation: Treat commands as examples, test in staging first, and apply one measured change at a time. <br>
Risk: Load tests, benchmarks, snapshots, and diagnostic dumps may disrupt services or expose sensitive operational data. <br>
Mitigation: Run production load tests only with approval and protect collected snapshots, benchmark output, and diagnostic dumps. <br>


## Reference(s): <br>
- [Performance Mastery release page](https://clawhub.ai/husttsq/performance-mastery) <br>
- [Benchmarking tools](references/benchmarking.md) <br>
- [C/C++ performance analysis and optimization](references/c_cpp_performance.md) <br>
- [Linux performance case studies](references/case_studies.md) <br>
- [Compiler optimization](references/compile_optimization.md) <br>
- [Container and Kubernetes performance](references/container_k8s.md) <br>
- [CPU performance](references/cpu.md) <br>
- [Disk I/O tuning](references/disk_io.md) <br>
- [eBPF and bpftrace](references/ebpf_bpftrace.md) <br>
- [Go performance](references/go_performance.md) <br>
- [Java performance](references/java_performance.md) <br>
- [Kernel parameters](references/kernel_params.md) <br>
- [Memory performance](references/memory.md) <br>
- [Network tuning](references/network.md) <br>
- [Node.js performance](references/nodejs_performance.md) <br>
- [Python performance](references/python_performance.md) <br>
- [Rust performance](references/rust_performance.md) <br>
- [Performance tool output guide](references/tool_output_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, diagnostic checklists, configuration snippets, and benchmark comparison guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose privileged Linux, container, sysctl, systemd, udev, fstab, and benchmark commands that require human review before execution.] <br>

## Skill Version(s): <br>
3.8.1 (source: server release metadata; artifact frontmatter reports 3.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
