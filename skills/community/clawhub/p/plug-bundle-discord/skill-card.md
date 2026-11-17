## Description:

discord组合包 bundles four communication skills for Discord, Discord Voice, 163.com email, and Telegram to help agents collect, process, and consolidate messages across communication channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this bundle to coordinate communication workflows across Discord, Discord voice, 163.com email, and Telegram while combining read, execution, and write capabilities into one workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, write, and execution-style authority across communication services may expose messages or allow unintended sends.

Mitigation: Install only with minimum-permission API keys and confirm which accounts and channels each member skill can access before use.

Risk: Sensitive chats, email, attachments, tokens, or credentials may be exposed through generic examples, prompts, or logs.

Mitigation: Avoid sending sensitive communication content or secrets through sample inputs and redact outputs before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-discord)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include communication-service API calls, account credential setup, and message or file outputs depending on member skill configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
