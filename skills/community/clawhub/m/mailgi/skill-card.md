## Description: <br>
Mailgi lets agents register email addresses and use Mailgi's API, SDK, or CLI to send, receive, read, organize, and manage mail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oyagev](https://clawhub.ai/user/oyagev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a Mailgi mailbox for task-related email workflows, including registration, inbox reads, message sending, mailbox organization, and API key management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to read, send, delete mail, organize mailbox state, and manage API keys. <br>
Mitigation: Limit inbox reads to the task at hand, review recipients and message content before sending, and require explicit confirmation before deleting mail, changing mailbox state, or revoking API keys. <br>
Risk: Mailgi API keys and DID-based tokens are sensitive credentials that can grant mailbox access. <br>
Mitigation: Keep keys private, store the one-time registration API key immediately in a secure location, and create scoped or task-specific keys where practical. <br>


## Reference(s): <br>
- [Mailgi ClawHub listing](https://clawhub.ai/oyagev/mailgi) <br>
- [Mailgi skill instructions](artifact/SKILL.md) <br>
- [Mailgi API base URL](https://api.mailgi.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with REST examples, JSON payloads, bash commands, TypeScript snippets, and CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mailgi API key or optional DID-based token; sending is limited to 100 external emails per day per API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
