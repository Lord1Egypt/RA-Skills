## Description:

Runs an OpenClaw meta-harness evolution loop that reads Hoss workspace configuration, proposes targeted harness edits, evaluates candidates against benchmark scenarios, logs results, and posts a research summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylerdotai](https://clawhub.ai/user/tylerdotai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run nightly or manually triggered experiments that evolve Hoss/OpenClaw harness configuration, compare candidates with a benchmark, and keep an evolution history for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated sub-agents can propose changes to core OpenClaw/Hoss configuration files.

Mitigation: Run the skill first in an isolated test workspace and require human review before promoting candidate harness files into a live agent workspace.

Risk: Workspace configuration and proposer reasoning may include sensitive context that could be exposed in logs or Discord summaries.

Mitigation: Remove or redact secrets from TOOLS.md and proposer traces, and disable Discord posting unless explicitly needed.

Risk: Benchmark-driven evolution can overfit to the bundled scenarios or introduce low-quality behavior outside the benchmark.

Mitigation: Review candidate diffs, keep benchmark scenarios diverse, and scan each selected harness before deployment.

## Reference(s):

- [Harness Spec](references/harness-spec.md)
- [Benchmark Design](references/benchmark-design.md)
- [Evolution Logic](references/evolution-logic.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON logs, candidate configuration files, benchmark scores, and Discord-ready summary text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes candidate harness files, evaluation scores, traces, and run history under ~/hoss-evolution/ when executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
