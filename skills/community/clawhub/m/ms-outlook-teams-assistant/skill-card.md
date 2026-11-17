## Description:

Track Microsoft Outlook email and optional Microsoft Teams messages on a Windows machine, generate reminders for items needing replies, draft concise email replies, and surface action items from recent messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinavjp](https://clawhub.ai/user/abhinavjp)

### License/Terms of Use:


## Use Case:

Employees and individual operators use this skill to monitor recent Outlook email and optional Teams messages, identify items that may need a reply, generate reminder text, and draft short Outlook replies for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent Outlook email and optional Teams messages that may contain sensitive workplace content.

Mitigation: Use it only on trusted local Windows machines and grant the narrowest Microsoft Graph scopes that still support the intended workflow.

Risk: Local config, scan cache, state, and Teams token cache files may contain message data or token material.

Mitigation: Keep those files out of source control and backups, restrict local file access, and secure or relocate the token cache.

Risk: Reminder text may include workplace message excerpts and may be sent to Telegram or another external channel.

Mitigation: Require user review before sending reminders externally, or use an approved internal channel when workplace data must stay inside the tenant.

## Reference(s):

- [Configuration example](references/config.example.json)
- [Teams via Microsoft Graph setup](references/teams-graph-setup.md)
- [Writing style](references/writing-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON scan results, and plain-text reminder or draft content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON state, scan caches, thread context, and optional Outlook draft containers; it does not auto-send email or Teams messages.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
