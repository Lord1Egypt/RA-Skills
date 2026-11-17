## Description:

Manage PagerDuty incidents, on-call schedules, escalation policies, and services via the PagerDuty REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and on-call responders use this skill to inspect PagerDuty state and run incident operations such as acknowledge, resolve, trigger, snooze, note, and reassign.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live PagerDuty incident state with an API key.

Mitigation: Use the least-privileged PagerDuty token available and require explicit human confirmation before acknowledge, resolve, trigger, snooze, or reassign commands.

Risk: PagerDuty credentials may be exposed or persist in shared environments.

Mitigation: Avoid storing the token in shared shell profiles, keep it out of logs and prompts, and rotate it regularly.

Risk: The security review notes limited built-in safeguards and credential-handling guidance.

Mitigation: Review the command and target incident before execution and deploy the skill only where PagerDuty access is appropriate.

## Reference(s):

- [PagerDuty REST API](https://api.pagerduty.com)
- [PagerDuty Events API v2](https://events.pagerduty.com/v2/enqueue)
- [ClawHub Skill Page](https://clawhub.ai/fr3kstyle/skills/pagerduty-oncall)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PagerDuty API credentials for live API operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
