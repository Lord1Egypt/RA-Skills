## Description:

Manage PagerDuty incidents, on-call schedules, services, and maintenance windows directly from your agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbotworker](https://clawhub.ai/user/clawdbotworker)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to inspect PagerDuty incidents, on-call schedules, services, and maintenance windows from an agent workflow. With appropriate credentials and human approval, it can also create, acknowledge, resolve, annotate, and schedule maintenance for live PagerDuty resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live PagerDuty incident and alerting state.

Mitigation: Require explicit human approval before commands that create incidents, acknowledge or resolve incidents, add incident notes, or create maintenance windows.

Risk: The PagerDuty API key could be sent to an arbitrary or unencrypted endpoint if PAGERDUTY_BASE_URL is set.

Mitigation: Keep PAGERDUTY_BASE_URL unset unless the code is changed to restrict requests to HTTPS PagerDuty-controlled hosts.

Risk: Broad PagerDuty credentials could grant more access than the workflow needs.

Mitigation: Use a least-privilege PagerDuty API key scoped to the intended account and operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdbotworker/skills/pagerduty-agent)
- [Publisher profile](https://clawhub.ai/user/clawdbotworker)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)
- [PagerDuty REST API endpoint](https://api.pagerduty.com)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Structured JSON responses on stdout, with setup and invocation examples in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and PAGERDUTY_API_KEY; PAGERDUTY_FROM_EMAIL is required for write operations.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
