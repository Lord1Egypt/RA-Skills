## Description:

Run PinchBench benchmarks to evaluate OpenClaw agent performance across real-world tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olearycrew](https://clawhub.ai/user/olearycrew)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use PinchBench to run real-world benchmark tasks against OpenClaw agents, compare model performance, save local result files, and optionally submit scores to the public PinchBench leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark execution runs embedded grading code from task files.

Mitigation: Review task automated checks as code before running and execute benchmarks only in an isolated workspace.

Risk: Benchmark results can be uploaded to the PinchBench leaderboard and may include telemetry about task outcomes and usage.

Mitigation: Use --no-upload for private runs and only register or upload when public leaderboard submission is intended.

Risk: PINCHBENCH_SERVER_URL can redirect registration or uploads to a custom endpoint.

Mitigation: Leave PINCHBENCH_SERVER_URL unset unless the endpoint is trusted.

Risk: Benchmark setup deletes stored session history for bench-* OpenClaw agents.

Mitigation: Run with dedicated benchmark agents and preserve any needed session history before starting a benchmark.

Risk: One benchmark task may install an external humanizer skill from the registry.

Mitigation: Review that task before use, skip it when appropriate, or install only a trusted humanizer skill.

## Reference(s):

- [PinchBench Homepage](https://pinchbench.com)
- [PinchBench Skill Repository](https://github.com/pinchbench/skill)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/olearycrew/skills/pinchbench)
- [uv Package Manager](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, json]

**Output Format:** [Markdown guidance, shell command examples, and JSON benchmark result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Benchmark runs may optionally upload summarized results to the PinchBench leaderboard unless run with --no-upload.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter; pyproject.toml lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
