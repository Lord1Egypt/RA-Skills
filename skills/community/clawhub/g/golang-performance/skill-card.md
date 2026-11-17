## Description:

Golang performance optimization patterns and methodology - if X bottleneck, then apply Y. Covers allocation reduction, CPU efficiency, memory layout, GC tuning, pooling, caching, and hot-path optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review and optimize Go services after profiling or benchmarking identifies a performance bottleneck. It guides allocation reduction, CPU efficiency, runtime tuning, caching, I/O optimization, observability, and benchmark comparison workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests authority to read and edit Go code, run Go performance tools, and use outbound network capability.

Mitigation: Install only in repositories where those actions are acceptable, use sandboxing for untrusted code, and review proposed code or command changes before applying them.

Risk: Profiling and production build examples can expose sensitive runtime data or affect production systems if used without controls.

Mitigation: Do not expose pprof publicly, avoid production SSH build workflows outside controlled CI or staging environments, and follow the release security guidance.

Risk: Installing benchstat with an unpinned latest version can change tool behavior over time.

Mitigation: Pin benchstat to a reviewed version when reproducibility or supply-chain control is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-performance)
- [Publisher Profile](https://clawhub.ai/user/samber)
- [Project Homepage](https://github.com/samber/cc-skills-golang)
- [Caching Patterns](references/caching.md)
- [CPU Optimization](references/cpu.md)
- [I/O & Networking Optimization](references/io-networking.md)
- [Memory Optimization](references/memory.md)
- [Production Observability for Performance](references/observability.md)
- [Runtime Tuning](references/runtime.md)
- [Example Prometheus Alerts](assets/prometheus-alerts.yml)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go code changes, benchmark commands, profiler commands, configuration changes, and review findings.]

## Skill Version(s):

1.3.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
