## Description:

Analyze OpenClaw configs and session data to recommend specific, cost-effective token usage and model tuning changes with clear trade-offs and explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marc4211](https://clawhub.ai/user/marc4211)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use OptimoClaw to inspect actual OpenClaw configuration and session usage, estimate token costs, and choose reviewed configuration changes that reduce spend while preserving needed quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw configuration and usage outputs can reveal operational details such as profile names, model identifiers, gateway connection details, and session usage.

Mitigation: Review gathered CLI output before sharing it outside trusted channels and exclude unrelated sensitive context from analysis requests.

Risk: Suggested OpenClaw configuration commands can change model routing, heartbeat frequency, concurrency, or context behavior if executed.

Mitigation: Treat commands as proposals and review cost, quality, rate-limit, and context trade-offs before running them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates are based on user-provided OpenClaw CLI JSON outputs and embedded rate card values; configuration commands are recommendations for user review.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
