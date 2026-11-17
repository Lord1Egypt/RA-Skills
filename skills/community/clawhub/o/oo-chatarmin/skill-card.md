## Description:

Chatarmin (chatarmin.com). Use this skill for ANY Chatarmin request — reading, creating, updating, and deleting data. Whenever a task involves Chatarmin, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to read and manage Chatarmin contacts, campaigns, flows, vouchers, and webhooks, and to send WhatsApp messages through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can execute unverified software; external installer contents and the exact downloaded CLI build were not verified.

Mitigation: Review the CLI setup, prefer a verified fixed release, and disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED before first invocation when only Chatarmin access is needed.

Risk: Startup skill synchronization may introduce undisclosed changes to other agents’ skills.

Mitigation: Disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED when only Chatarmin access is needed.

Risk: Sending messages and changing or deleting Chatarmin data can affect the connected account.

Mitigation: Connect only the intended account and obtain approval for message sending, changes, and deletions.

## Reference(s):

- [Chatarmin API documentation](https://apidocs.chatarmin.com/reference/api-overview)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Chatarmin homepage](https://chatarmin.com/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON request payloads and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and payloads depend on the selected Chatarmin action and its live input schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
