## Description:

Monitor and report usage, costs, quotas, and rate limits for LLM providers, plus manage clawmeter setup and daemon status securely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielithomas](https://clawhub.ai/user/danielithomas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check LLM provider usage, spend, quotas, rate limits, and clawmeter setup or daemon status without exposing credentials to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned clawmeter package.

Mitigation: Install and approve a pinned, verified clawmeter version before using the skill for monitoring tasks.

Risk: The skill may create persistent local monitoring configuration and manage a background daemon.

Mitigation: Require explicit confirmation before configuration writes, daemon starts, service installation, or history purge actions.

Risk: The skill collects and reports local LLM usage history.

Mitigation: Use it only where local usage monitoring is acceptable, and review retention and history settings before enabling collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielithomas/skills/llm-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown with command snippets and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarises provider usage and warns before credential handling, service installation, daemon starts, config writes, or destructive history actions.]

## Skill Version(s):

0.7.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
