## Description:

Microsoft Teams (microsoft.com). Use this skill for ANY Microsoft Teams request — reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Teams users can use the skill to read Teams profiles, teams, channels, chats, and messages, and to send or reply to messages through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute an unverified installer and automatic skill synchronization can make broader agent changes.

Mitigation: Review software setup separately, prefer a verified pinned CLI release, and disable automatic skill synchronization if you do not want other agent skills changed.

Risk: Sending or replying to Teams messages changes account data, and a connected account may have broad permissions.

Mitigation: Limit the connected Teams account's permissions and retain the required confirmation before sending messages.

## Reference(s):

- [Microsoft Teams overview](https://www.microsoft.com/microsoft-365/microsoft-teams/group-chat-software)
- [Microsoft Graph Teams overview](https://learn.microsoft.com/en-us/graph/teams-concept-overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read Teams data or send channel and chat messages.]

## Skill Version(s):

1.0.2 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
