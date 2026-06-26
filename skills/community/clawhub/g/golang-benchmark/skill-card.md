## Description: <br>
Guides agents through Go benchmarking, profiling, benchmark comparison, CI regression detection, and production performance investigation using Go tools such as pprof, trace, and benchstat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to write and run Go benchmarks, interpret profiles and traces, compare before/after performance, and set up regression checks for Go projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: pprof or trace endpoints can expose operational details when used against real services. <br>
Mitigation: Restrict access to profiling endpoints and avoid exposing them publicly. <br>
Risk: Profiles and traces can contain stack traces, identifiers, paths, and other sensitive operational information. <br>
Mitigation: Review and redact captured benchmark, profile, and trace artifacts before sharing them. <br>
Risk: Insecure TLS settings can weaken safety when collecting production performance data. <br>
Mitigation: Use secure transport settings and avoid disabling TLS verification during profiling or metric collection. <br>


## Reference(s): <br>
- [Golang Benchmark on ClawHub](https://clawhub.ai/samber/golang-benchmark) <br>
- [Publisher Profile](https://clawhub.ai/user/samber) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [benchstat Reference](references/benchstat.md) <br>
- [CI Benchmark Regression Detection](references/ci-regression.md) <br>
- [Compiler Analysis Reference](references/compiler-analysis.md) <br>
- [Investigation Session Setup](references/investigation-session.md) <br>
- [pprof Reference](references/pprof.md) <br>
- [Prometheus Go Runtime Metrics Reference](references/prometheus-go-metrics.md) <br>
- [Diagnostic Tools Quick Reference](references/tools.md) <br>
- [Execution Trace Reference](references/trace.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Go code examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include benchmark commands, pprof and trace workflows, benchstat interpretation, CI regression guidance, and reviewable code or configuration changes.] <br>

## Skill Version(s): <br>
1.2.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
