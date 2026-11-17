## Description:

A/B testing and feature optimization for AI agents that picks the best option automatically using Multi-Armed Bandits and Contextual Bandits (LinUCB), with no data warehouse needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose the best variant from multiple options, run A/B tests without fixed sample sizes, and make context-aware selections for prompts, feature flags, email subjects, or similar choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned MCP command, and the actual MCP server code is not included in the artifact for review.

Mitigation: Use only a verified OraClaw MCP server source, pin dependencies or disable runtime npx installation, and run the MCP process with the minimum environment and file access needed.

## Reference(s):

- [OraClaw Bandit homepage](https://oraclaw.dev/bandit)
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-bandit)
- [ClawHub publisher profile](https://clawhub.ai/user/whatsonyourmind)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API calls]

**Output Format:** [Markdown with JSON configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and an OraClaw MCP server connection; optimization calls may incur usage-based pricing.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
