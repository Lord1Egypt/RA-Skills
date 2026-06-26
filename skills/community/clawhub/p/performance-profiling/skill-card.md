## Description: <br>
性能分析速查。当需要：(1) Python 性能分析 (2) Node.js 性能分析 (3) 数据库优化 (4) 系统性能监控时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afine907](https://clawhub.ai/user/afine907) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill as a quick reference for profiling Python and Node.js applications, investigating database performance, monitoring system resources, and planning controlled web load tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Load-test commands can generate disruptive traffic against web services. <br>
Mitigation: Run tests only against systems you own or are authorized to test, start with low concurrency, and avoid production without an approved maintenance window. <br>
Risk: Database commands include query termination and Redis log-reset operations that can affect active workloads or observability. <br>
Mitigation: Require explicit operator review before using production-impacting database commands and prefer read-only inspection commands first. <br>
Risk: Profiling and monitoring commands may expose process, query, or memory details from sensitive environments. <br>
Mitigation: Use controlled environments when possible and review captured profiling output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afine907/performance-profiling) <br>
- [Python profiling documentation](https://docs.python.org/3/library/profile.html) <br>
- [clinic.js](https://clinicjs.org/) <br>
- [FlameGraph](https://www.brendangregg.com/flamegraphs.html) <br>
- [FlameGraph source](https://github.com/brendangregg/FlameGraph) <br>
- [Python performance profiling reference](references/python.md) <br>
- [Node.js performance profiling reference](references/nodejs.md) <br>
- [Database optimization reference](references/database.md) <br>
- [System performance reference](references/system.md) <br>
- [Web load testing reference](references/load-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes copy-paste profiling, database inspection, system monitoring, and load-test commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
