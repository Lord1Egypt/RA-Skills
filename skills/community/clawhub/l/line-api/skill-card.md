## Description:

Line Client enables an agent to authenticate with QR login, send and read LINE messages, and manage contacts, groups, profiles, reactions, polling, and settings through a Chrome extension gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2manslkh](https://clawhub.ai/user/2manslkh)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent operate a LINE account for messaging, contact, group, profile, reaction, polling, and settings workflows after QR-code authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or act on private LINE messages, contacts, groups, profile details, and settings.

Mitigation: Require explicit confirmation before reading private chats or changing messages, contacts, groups, profile, settings, or group membership.

Risk: The token and certificate cache files are account credentials.

Mitigation: Protect ~/.line-client/tokens.json and ~/.line-client/sqr_cert, and keep them out of logs, shared output, backups, and source control.

Risk: The skill depends on an external repository and WASM signer for authenticated API access.

Mitigation: Review the external repository and WASM signer before use, especially before allowing account-changing operations.

Risk: QR login requires a user-scanned code and time-sensitive PIN.

Mitigation: Relay QR and PIN material through a trusted channel, avoid logging it, and abandon stale authentication attempts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2manslkh/skills/line-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API method names, QR login steps, token file paths, and safety guidance.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
