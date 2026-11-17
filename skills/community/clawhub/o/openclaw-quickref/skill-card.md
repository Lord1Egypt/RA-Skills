## Description:

Provides a quick reference for OpenClaw CLI commands, configuration syntax, and common usage patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxadc](https://clawhub.ai/user/maxadc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer OpenClaw CLI and configuration questions, including command syntax, config paths, provider settings, and common patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference includes destructive OpenClaw command examples such as session deletion, plugin removal, config unset, and node unpairing.

Mitigation: Require explicit user confirmation before proposing or executing destructive OpenClaw commands.

Risk: Some configuration examples involve API keys and provider credentials.

Mitigation: Prefer environment-variable references and avoid placing real API keys directly in shell commands or configuration snippets.

Risk: Broad quick-reference activation can produce outdated or misleading command guidance if the local OpenClaw version differs from the examples.

Mitigation: Treat generated answers as quick-reference guidance and verify commands against the local OpenClaw CLI help or configuration before execution.

## Reference(s):

- [OpenClaw CLI Command Reference](artifact/references/cli-reference.md)
- [OpenClaw Configuration Reference](artifact/references/config-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/maxadc/skills/openclaw-quickref)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw CLI commands and configuration snippets; sensitive keys should be represented as environment-variable references.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
