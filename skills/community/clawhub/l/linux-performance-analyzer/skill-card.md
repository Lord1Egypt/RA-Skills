## Description: <br>
Linux Performance Analyzer helps agents diagnose and tune Linux CPU, memory, disk I/O, network, kernel parameter, compiler optimization, and container/Kubernetes performance issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[husttsq](https://clawhub.ai/user/husttsq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site reliability engineers use this skill to collect Linux performance evidence, identify bottlenecks, draft incident reports, and plan tested tuning changes with validation and rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Admin-level Linux tuning examples can disrupt production systems if copied directly or run with broad privileges. <br>
Mitigation: Do not give the agent root access by default; record current values, test temporary changes first, use maintenance windows for persistent changes, and keep rollback steps. <br>
Risk: Performance snapshots, process lists, network details, kernel logs, and heap dumps can contain sensitive operational data. <br>
Mitigation: Treat collected diagnostics as sensitive and redact or restrict them before sharing outside the intended operations team. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/husttsq/linux-performance-analyzer) <br>
- [CPU tuning reference](references/cpu.md) <br>
- [Memory tuning reference](references/memory.md) <br>
- [Disk I/O tuning reference](references/disk_io.md) <br>
- [Network tuning reference](references/network.md) <br>
- [Kernel parameter reference](references/kernel_params.md) <br>
- [Compiler optimization reference](references/compile_optimization.md) <br>
- [Linux performance case studies](references/case_studies.md) <br>
- [Brendan Gregg Linux Performance](http://www.brendangregg.com/linuxperf.html) <br>
- [Brendan Gregg perf Examples](http://www.brendangregg.com/perf.html) <br>
- [ESnet Linux TCP Tuning](https://fasterdata.es.net/host-tuning/linux/) <br>
- [sysctl Explorer](https://sysctl-explorer.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with diagnostic tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include analysis reports, command recommendations, tuning snippets, validation checks, and rollback steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
