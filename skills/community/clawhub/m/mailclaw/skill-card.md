## Description:

MailClaw helps users manage Gmail by creating email automation rules, reviewing pre-analyzed digests, and sending user-confirmed actions to connected apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tourmind](https://clawhub.ai/user/tourmind)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use MailClaw to triage Gmail, create persistent email rules, review summarized inbox digests, and route confirmed actions to Gmail, Slack, Notion, Google Calendar, Linear, and HubSpot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests ongoing Gmail and connected-app access for inbox automation.

Mitigation: Install only after confirming trust in the MailClaw backend and verifying that Gmail and connected-app access can be revoked.

Risk: The skill stores a MailClaw API key locally and uses it for subsequent API requests.

Mitigation: Protect the local configuration file, prefer a pinned install, and rotate or revoke the key if the workspace is shared or compromised.

Risk: Gmail-derived summaries or content may be sent to Slack, Notion, Google Calendar, Linear, HubSpot, or Gmail actions.

Mitigation: Review each proposed action and destination before confirmation, especially for sensitive email content.

Risk: Heartbeat tasks can poll for new email and generate digest links on a schedule.

Mitigation: Verify the schedule is expected, confirm the API domain, and ensure heartbeat tasks can be disabled when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tourmind/skills/mailclaw)
- [MailClaw API base URL](https://concentrate-patent-cent-sent.trycloudflare.com)
- [MailClaw dashboard](https://aauth-170125614655.asia-northeast1.run.app/dashboard)
- [README.md](artifact/README.md)
- [HEARTBEAT.md](artifact/HEARTBEAT.md)
- [setup.md](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces conversational setup guidance, email digest cards, rule configuration bodies, OAuth links, verification codes, and user-confirmed action prompts.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
