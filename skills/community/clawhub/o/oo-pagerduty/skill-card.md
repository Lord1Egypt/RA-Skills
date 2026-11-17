## Description:

PagerDuty (pagerduty.com). Use this skill for ANY PagerDuty request — reading, creating, updating, and deleting data. Whenever a task involves PagerDuty, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and on-call responders use this skill to retrieve PagerDuty incident, user, and on-call data, and to acknowledge, update, or resolve incidents through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags incident resolution as potentially lacking confirmation.

Mitigation: Require confirmation for every state-changing action and maintain an explicit allowlist for reads.

Risk: The remote CLI installer and live connector implementation were not verified by the security review.

Mitigation: Install the CLI through a reviewed, verified method and consider the access granted to OOMOL.

## Reference(s):

- [PagerDuty API documentation](https://developer.pagerduty.com/api-reference)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-pagerduty)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance, Shell commands]

**Output Format:** [JSON connector payloads and results with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by PagerDuty action.]

## Skill Version(s):

1.0.5 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
