## Description:

Estimates and logs subagent spawn costs, presents approval gates for higher-cost tasks, and summarizes daily or monthly spend for OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators using OpenClaw multi-agent workflows use this skill to estimate subagent costs before spawning, log estimated and actual spend, and review budget status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be interpreted as hard billing protection even though the security review describes it as an advisory estimator and logger.

Mitigation: Review the skill before installation and add an enforced wrapper around subagent spawning before relying on it to stop spend.

Risk: Persistent cost logs can capture sensitive task details.

Mitigation: Avoid storing secrets or sensitive task descriptions in cost-tracking.md and restrict access to the workspace notes directory.

Risk: The documented budget cap may not stop spending unless the surrounding agent runtime enforces it.

Mitigation: Verify budget-cap behavior in the target environment and monitor provider billing dashboards for actual spend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/skills/openclaw-cost-governor)
- [Publisher profile](https://clawhub.ai/user/donovanpankratz-del)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and cost summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates depend on configured model rates, task multipliers, and manual reconciliation of actual spend.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
