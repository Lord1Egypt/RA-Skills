## Description: <br>
Manage PagerDuty incidents, services, schedules, escalation policies, users, and on-call data via the PagerDuty REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, reliability, and incident-response teams use this skill to inspect PagerDuty incidents and related service, schedule, escalation, user, and on-call data, then perform user-confirmed incident-management actions through ClawLink. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to PagerDuty through ClawLink and can access account incident-management data. <br>
Mitigation: Review the ClawLink connection and PagerDuty permissions before use, and install only when the user is comfortable with that connection. <br>
Risk: Confirmed write actions can change real on-call operations, including incident status, escalations, schedules, services, or users. <br>
Mitigation: Preview and explicitly confirm the target resource and intended effect before any create, update, delete, escalation, reassignment, or schedule action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/pagerduty-incidents) <br>
- [PagerDuty REST API Reference](https://developer.pagerduty.com/api-reference/) <br>
- [PagerDuty Incidents API](https://developer.pagerduty.com/api-reference/rZMyfN/incidents/) <br>
- [PagerDuty Services API](https://developer.pagerduty.com/api-reference/R4FyWD/services/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing instructions and ClawLink tool-call guidance; write operations should be previewed and explicitly confirmed.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
