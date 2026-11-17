## Description:

Track Chinese packages with the Kuaidi100 API, receive push updates, manage tracked packages, and create Google Calendar delivery reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rou-assistant-bot](https://clawhub.ai/user/rou-assistant-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to subscribe package tracking numbers to Kuaidi100 push updates, review locally cached delivery state, and sync same-day delivery reminders to Google Calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public webhook can accept weakly authenticated package updates that may change local package state or trigger Google Calendar changes.

Mitigation: Use a high-entropy webhook token, configure a callback salt, and set webhook.signatureMode to strict before exposing the webhook publicly.

Risk: Package numbers, notes, delivery status, and recent tracking context may be stored locally and shared with Kuaidi100 or Google Calendar as part of normal operation.

Mitigation: Limit tracked package data to what is needed, protect local state files, and use dedicated credentials with the minimum required calendar access.

## Reference(s):

- [Kuaidi100 API](https://api.kuaidi100.com)
- [Kuaidi100 Subscribe API](https://api.kuaidi100.com/document/subscribeApi)
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with configuration examples and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Kuaidi100 and Google Calendar APIs and may read or update local package tracking state during normal operation.]

## Skill Version(s):

1.0.0 (source: evidence release and openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
