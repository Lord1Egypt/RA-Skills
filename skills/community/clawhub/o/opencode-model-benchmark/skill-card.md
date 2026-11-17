## Description:

Benchmarks free models on OpenCode Zen by calling the public API, measuring response time and tokens per second, and returning a ranked Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braveheartzjh](https://clawhub.ai/user/braveheartzjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare current free OpenCode Zen model latency, token usage, and generation speed from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to opencode.ai to fetch model documentation and run benchmark prompts.

Mitigation: Install and run it only in environments where outbound OpenCode network access is acceptable.

Risk: Benchmark results may change with model availability, rate limits, and network conditions.

Mitigation: Treat results as a point-in-time comparison and rerun the benchmark before using results for model selection.

## Reference(s):

- [OpenCode Zen documentation](https://opencode.ai/docs/zh-cn/zen)
- [OpenCode Zen API endpoint](https://opencode.ai/zen/v1)
- [ClawHub skill page](https://clawhub.ai/braveheartzjh/skills/opencode-model-benchmark)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Analysis]

**Output Format:** [Markdown report printed to stdout with tabular benchmark results and a terminal summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files are written; results depend on current OpenCode model availability and network latency.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
