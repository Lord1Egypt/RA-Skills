## Description:

Provides real-time Home Assistant monitoring, alert rules, Echo voice notifications, Telegram delivery, entity inspection, and opt-in service calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincsta](https://clawhub.ai/user/vincsta)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Home Assistant users use this skill to monitor device states, define alert rules, inspect entities, send Telegram or Echo notifications, and execute explicitly allowed Home Assistant service calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Home Assistant and Telegram credentials may be exposed through local configuration or unencrypted Home Assistant connections.

Mitigation: Use HTTPS/WSS, store secrets only in a gitignored config file with restricted permissions, and rotate long-lived tokens if exposure is suspected.

Risk: Allowed service-call domains can change physical devices and may permit broader automation effects than intended.

Mitigation: Keep service calls disabled until needed, remove scene and automation from call_safe_domains unless fully audited, and test changes with dry-run first.

Risk: Alert messages sent to Telegram or Echo devices can reveal household state, occupancy, routines, or other sensitive context.

Mitigation: Avoid sensitive personal data in templates and route notifications only to trusted Telegram chats and intended Echo devices.

Risk: The provided start script can stop unintended processes because of broad pkill matching.

Mitigation: Avoid start.sh until its process matching is narrowed, and verify process state before stopping background services.

## Reference(s):

- [Home Assistant Hub setup guide](references/setup.md)
- [ClawHub skill page](https://clawhub.ai/vincsta/skills/home-assistant-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Home Assistant service-call examples, alert-rule definitions, setup steps, and operational guidance that should be reviewed before execution.]

## Skill Version(s):

1.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
