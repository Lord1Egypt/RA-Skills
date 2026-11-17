## Description:

Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabrielsayumi](https://clawhub.ai/user/gabrielsayumi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent operate wacli for user-directed WhatsApp messaging, chat discovery, history search, sync, and backfill. It is intended for explicit requests to contact third parties or inspect WhatsApp history, not for routine chats with the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access WhatsApp authentication state and message history through wacli.

Mitigation: Install only after trusting the upstream wacli package, prefer a pinned or reviewed release, and limit use to expected WhatsApp accounts and stores.

Risk: A mistaken recipient, message, or file path could send unintended WhatsApp content.

Mitigation: Require an explicit recipient and message or file, confirm the action before sending, and ask a clarifying question when details are ambiguous.

Risk: History backfill may be incomplete because it requires the phone to be online and returns best-effort results.

Mitigation: Treat backfill results as incomplete unless independently confirmed, and communicate uncertainty when using recovered history.

## Reference(s):

- [PROBAR on ClawHub](https://clawhub.ai/gabrielsayumi/skills/probar)
- [wacli homepage](https://wacli.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command suggestions when machine-readable wacli output is useful.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
