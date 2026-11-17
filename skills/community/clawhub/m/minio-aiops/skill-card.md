## Description:

Supports MinIO operators with storage diagnostics and governed bucket, object-lock, and IAM operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

MinIO operators and storage engineers use this agent skill to inspect health, capacity, exposure, lifecycle, and healing, and to perform MinIO configuration changes with audit and undo support where available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious because it includes potentially destructive storage operations and has gaps in approval safeguards; the scan is incomplete.

Mitigation: Before installing, seek maintainer clarification on retention changes, permanent deletion, and approval for MCP writes. Until then, use least-privilege or read-only credentials and require a human to review any write operation.

## Reference(s):

- [Project homepage](https://github.com/AIops-tools/MinIO-AIops)
- [Capabilities reference](references/capabilities.md)
- [Setup and security guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions, Shell commands, JSON]

**Output Format:** [Plain-language analysis and guidance, JSON tool results, and Markdown with shell commands or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results may be bounded or truncated; the skill reports truncation indicators where applicable.]

## Skill Version(s):

0.15.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
