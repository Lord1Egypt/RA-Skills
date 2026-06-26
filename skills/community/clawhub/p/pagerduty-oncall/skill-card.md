## Description: <br>
Manage PagerDuty incidents, on-call schedules, escalation policies, and services via the PagerDuty REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident responders use this skill to inspect PagerDuty incidents, on-call schedules, escalation policies, and services, then run approved incident-management actions through the PagerDuty API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent live incident-management power, including acknowledge, resolve, trigger, snooze, reassign, note, and direct API actions. <br>
Mitigation: Require explicit human approval before live PagerDuty write actions or direct curl API calls. <br>
Risk: PagerDuty API and integration keys can expose operational control if logged, pasted into chat, or over-permissioned. <br>
Mitigation: Use a least-privileged PagerDuty token limited to the services the agent should manage and protect API and integration keys from logs or chat transcripts. <br>


## Reference(s): <br>
- [PagerDuty REST API](https://api.pagerduty.com) <br>
- [PagerDuty Events API v2](https://events.pagerduty.com/v2/enqueue) <br>
- [ClawHub release page](https://clawhub.ai/fr3kstyle/pagerduty-oncall) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PagerDuty API credentials from environment variables and may perform live incident actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
