## Description:

Use an OOMOL-connected Chat API for WhatsApp account to read chats and messages, inspect settings, and send text or files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use this skill to retrieve WhatsApp chats, messages, status, and settings through a connected Chat API account, or send a text message or file. The skill also guides first-time CLI and account setup when a relevant connection error occurs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified code and cause broader agent changes through skill synchronization.

Mitigation: Review setup first, prefer a separately verified fixed CLI release, approve local installation explicitly, and disable automatic synchronization if unwanted.

Risk: WhatsApp messages processed through OOMOL may have privacy implications; installer contents and the external runtime could not be verified.

Mitigation: Consider message privacy before connecting the account, and verify the installer and runtime before use.

## Reference(s):

- [Chat API for WhatsApp](https://chat-api.com/en/)
- [Chat API documentation](https://chat-api.com/en/docs.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Text, Guidance]

**Output Format:** [Structured JSON requests through the oo CLI and returned API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected Chat API account and the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
