## Description:

Manage PagerDuty incidents, services, schedules, escalation policies, users, and on-call data via the PagerDuty REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and incident responders use this skill to inspect PagerDuty state and manage incident workflows from an agent chat. It supports listing and updating incidents, services, schedules, escalation policies, users, and on-call data through the connected PagerDuty account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allow an unpinned third-party plugin that can mediate PagerDuty credentials and operational changes.

Mitigation: Use least-privilege PagerDuty access, review the plugin before installing, and prefer a pinned or verified ClawLink plugin release when available.

Risk: PagerDuty write operations can affect production incident response, escalation, schedules, services, or users.

Mitigation: Confirm every create, update, delete, reassignment, escalation, and schedule change with the user before execution.

## Reference(s):

- [PagerDuty REST API Reference](https://developer.pagerduty.com/api-reference/)
- [PagerDuty Incidents API](https://developer.pagerduty.com/api-reference/rZMyfN/incidents/)
- [PagerDuty Services API](https://developer.pagerduty.com/api-reference/R4FyWD/services/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live ClawLink PagerDuty tool catalog; write operations should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
