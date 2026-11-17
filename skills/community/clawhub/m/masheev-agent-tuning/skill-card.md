## Description:

Review and improve a Masheev AI agent from an AI assistant connected to the Masheev MCP server. Use when asked why the AI agent gave a wrong answer, to "improve my bot", tighten its instructions, add knowledge it is missing, pause or resume it, or check whether its channels are set up. Reads recent conversations and escalations as evidence, proposes concrete instruction or knowledge changes, and applies them only after the owner approves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masheev](https://clawhub.ai/user/masheev)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and operators use the skill to diagnose incorrect or incomplete customer-service replies from a Masheev AI agent, improve its instructions or knowledge, and check its setup and channels. It proposes focused changes and applies them only after the owner approves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant can access customer conversations and escalations in the connected Masheev workspace.

Mitigation: Connect only the intended workspace and grant only the permissions needed.

Risk: Approved changes can affect live customer replies.

Mitigation: Review proposed changes and retain the original instructions for rollback.

## Reference(s):

- [Masheev Agents Documentation](https://docs.masheev.com/agents)
- [ClawHub Skill Release](https://clawhub.ai/masheev/skills/masheev-agent-tuning)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Text]

**Output Format:** [Concise conversational text with proposed instruction or knowledge changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changes to agent instructions, knowledge sources, or running state require owner approval.]

## Skill Version(s):

0.2.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
