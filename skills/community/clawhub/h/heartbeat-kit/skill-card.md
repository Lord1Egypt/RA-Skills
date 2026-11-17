## Description:

Pre-built HEARTBEAT.md templates for common agent tasks: email checking, calendar monitoring, weather alerts, system health, news digests. Drop in and go.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to copy and customize HEARTBEAT.md templates for periodic agent checks across email, calendar, weather, system health, news, social notifications, and project status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heartbeat templates may surface sensitive email, calendar, location, or notification details in periodic agent reports.

Mitigation: Configure only the accounts, locations, repositories, and topics that should be monitored, and review report content expectations before enabling the heartbeat.

Risk: A copied HEARTBEAT.md can cause recurring background checks in a workspace where monitoring was not intended.

Mitigation: Install templates only in intended workspaces, set quiet hours and intervals deliberately, and remove the template when periodic checks are no longer needed.

## Reference(s):

- [Heartbeat Kit on ClawHub](https://clawhub.ai/theshadowrose/skills/heartbeat-kit)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Combined Lite Heartbeat Template](artifact/templates/combined-lite.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown templates with configuration comments and brief shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Templates are intended to be copied into a workspace as HEARTBEAT.md and customized with local account, location, schedule, and priority settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
