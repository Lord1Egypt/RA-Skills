## Description:

Reliable Nextcloud integration for Notes, Tasks, Calendar, Files, and Contacts (CardDAV-safe vCard handling with robust contact create/update).

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicyroots](https://clawhub.ai/user/juicyroots)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Nextcloud notes, tasks, calendar events, files, and contacts through OpenClaw. It is intended for environments where a configured Nextcloud account can safely support remote reads, writes, uploads, and deletes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Nextcloud credentials that may grant access to private account data.

Mitigation: Use a dedicated, revocable, least-privilege Nextcloud app password and keep credentials in environment variables or a local secret store.

Risk: Remote upload and delete commands can modify or remove account data, including unintended paths if requests are not reviewed.

Mitigation: Test on non-production data first, use explicit reviewed paths, review commands before execution, and verify mutations with follow-up reads where practical.

Risk: Unencrypted or redirected Nextcloud endpoints can expose credentials or data.

Mitigation: Configure an HTTPS-only NEXTCLOUD_URL and avoid untrusted redirects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juicyroots/skills/nextcloud-aio-oc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+, NEXTCLOUD_URL, NEXTCLOUD_USER, and NEXTCLOUD_TOKEN; binary file transfers use the Python helper.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
