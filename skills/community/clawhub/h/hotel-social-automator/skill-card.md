## Description:

Generate, review, and publish social media content through MCP with AgentAuth and workspace token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tourmind](https://clawhub.ai/user/tourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel marketing teams and their agents use this skill to generate, review, publish, schedule, and monitor social media posts for hotel brands across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule public social media content for a brand.

Mitigation: Require a final human preview and explicit approval before publish or schedule actions.

Risk: The workflow depends on workspace and user tokens that authorize brand-specific access.

Mitigation: Treat uk_* and hp_sk_* values as secrets and use the skill only in workspaces where those tokens are approved for the intended brand.

Risk: The security scan reports unsafe command and credential-handling guidance around a high-impact posting workflow.

Mitigation: Review before installing, validate image URLs before download, and use unique private temporary files for downloaded assets.

## Reference(s):

- [User Onboarding](references/user-onboarding.md)
- [Error Handling](references/error-handling.md)
- [Conversation Examples](references/conversation-examples.md)
- [Feishu Platform Sending Guide](references/feishu-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/tourmind/skills/hotel-social-automator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured tool-call guidance with inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated social copy, review prompts, publishing status summaries, and setup guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
