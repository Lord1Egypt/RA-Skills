## Description:

Golang benchmarking, profiling, and performance measurement for writing, running, comparing, profiling, interpreting, and tracking Go benchmark and production performance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create statistically sound Go benchmarks, compare results with benchstat, inspect pprof and trace data, and set up CI checks for performance regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes copy-ready privileged host tuning commands for dedicated benchmark runners.

Mitigation: Run host-tuning commands only on disposable dedicated benchmark runners with rollback, and avoid granting passwordless sudo to agents.

Risk: The skill discusses pprof, trace, and production diagnostic workflows that can expose sensitive runtime data or add overhead.

Mitigation: Prefer localhost, SSH tunnels, VPNs, mTLS, and authenticated access for diagnostics, and keep profiling or tracing short-lived and targeted.

Risk: The skill installs Go-based benchmark tools using latest-version package references.

Mitigation: Pin Go tool versions before use in shared or production-adjacent environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-benchmark)
- [Project Homepage](https://github.com/samber/cc-skills-golang)
- [pprof Reference](references/pprof.md)
- [benchstat Reference](references/benchstat.md)
- [Trace Reference](references/trace.md)
- [Diagnostic Tools Quick Reference](references/tools.md)
- [Compiler Analysis Reference](references/compiler-analysis.md)
- [CI Benchmark Regression Detection](references/ci-regression.md)
- [Investigation Session Setup](references/investigation-session.md)
- [Prometheus Go Metrics Reference](references/prometheus-go-metrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Go, shell, YAML, and PromQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend running Go benchmark, benchstat, pprof, trace, Prometheus, and CI regression commands; outputs should be reviewed before execution.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
