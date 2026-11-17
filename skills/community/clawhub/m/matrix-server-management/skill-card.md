## Description:

Manage the Tuwunel Matrix Homeserver for explicit administrative tasks such as registering users, creating rooms, managing room membership, sending messages, and uploading files through the media API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montycn](https://clawhub.ai/user/montycn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent is explicitly asked to administer a local Tuwunel Matrix homeserver, including user registration, room setup, membership management, Matrix messaging, and file delivery to the admin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority over Matrix users, rooms, messages, and file sharing.

Mitigation: Use it only after explicit user approval for registration, room creation, membership changes, messaging, and file uploads.

Risk: Messages or uploaded files could reach the wrong room members.

Mitigation: Verify the target room, recipients, user IDs, and file path before sending a message or uploading media.

Risk: Matrix registration tokens, passwords, access tokens, logs, or config exports could be exposed.

Mitigation: Redact sensitive content from logs and files, and never reveal tokens or passwords in chat or uploaded artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/montycn/skills/matrix-server-management)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Matrix media URIs for uploaded files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
