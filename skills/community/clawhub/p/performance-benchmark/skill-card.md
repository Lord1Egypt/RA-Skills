## Description:

Measures performance baselines, detects regressions, and compares stack alternatives before and after changes across page, API, build, and comparison workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to establish performance baselines, compare metrics before and after code changes, and catch regressions in web pages, APIs, build pipelines, and development feedback loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark and load-test commands can disrupt production or third-party systems if run without authorization.

Mitigation: Run benchmarks only against systems you are authorized to test, preferably local or staging environments.

Risk: Benchmark output stored in .benchmarks/ may reveal internal URLs, service names, latency data, or operational metrics.

Mitigation: Review .benchmarks/ before committing or sharing benchmark artifacts.

Risk: The skill depends on user-supplied tools, so measurements can be inconsistent across environments or tool choices.

Mitigation: Document the selected benchmark tool, versions, target environment, and workload when recording baselines.

## Reference(s):

- [Benchmark Integration and Best Practices](references/integration.md)
- [Benchmark Modes Detailed Reference](references/modes.md)
- [ClawHub skill page](https://clawhub.ai/djc00p/skills/performance-benchmark)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with inline shell commands and benchmark report summaries; baseline artifacts may be JSON under .benchmarks/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided benchmark tools such as k6, autocannon, hyperfine, or browser performance tooling; no benchmark runner is bundled.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
