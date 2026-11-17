## Description:

Send push notifications via ntfy.sh or a self-hosted ntfy server, including priorities, titles, tags, icons, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have agents compose ntfy CLI commands for urgent alerts, monitoring notifications, email summaries, and system health messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags a real-looking shared-secret ntfy topic and plaintext HTTP examples.

Mitigation: Replace example endpoints with private HTTPS ntfy URLs, rotate any exposed topic, and use ntfy authentication or access controls before installation.

Risk: Notifications can expose email bodies, credentials, tokens, or sensitive metadata to notification infrastructure and device lock screens.

Mitigation: Send only the minimum necessary alert text and avoid credentials, tokens, full email bodies, and sensitive metadata in notification payloads.

## Reference(s):

- [ntfy documentation](https://ntfy.sh/)
- [ClawHub skill page](https://clawhub.ai/genortg/skills/ntfy-cli)
- [Publisher profile](https://clawhub.ai/user/genortg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ntfy topic URLs, priority flags, titles, tags, click actions, and attachment options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
