## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill when a user explicitly asks to send a WhatsApp message to another person or to sync/search WhatsApp history through wacli. It is not intended for routine WhatsApp chat handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive personal, business, or third-party WhatsApp messages through sync, search, or local persistence.

Mitigation: Use it only when WhatsApp access is intentional, avoid broad sync or backfill unless necessary, and consider a scoped --store path or deleting ~/.wacli data when finished.

Risk: The skill can send WhatsApp messages to direct or group recipients, creating risk from ambiguous recipient or message text.

Mitigation: Require an explicit recipient and message, confirm both before sending, and ask a clarifying question when anything is ambiguous.

Risk: Backfill and sync can retrieve private history and may produce best-effort results that depend on the phone being online.

Mitigation: Limit backfill request and count values to the minimum needed, prefer targeted searches, and disclose uncertainty when results may be incomplete.

## Reference(s):

- [OpenClaw wacli Playbook on ClawHub](https://clawhub.ai/danielsinewe/skills/openclaw-wacli-playbook)
- [wacli homepage](https://wacli.sh)
- [Publisher profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation guidance for outbound messages and wacli command examples; commands can use --json when machine-readable CLI output is needed.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
