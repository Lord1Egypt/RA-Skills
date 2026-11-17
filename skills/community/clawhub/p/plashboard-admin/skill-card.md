## Description:

Manage plashboard templates and autonomously convert natural-language dashboard requests into plashboard tool actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhytabest](https://clawhub.ai/user/jhytabest)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to administer Plashboard templates, activate dashboards, run updates, inspect status, and turn natural-language dashboard requests into Plashboard tool actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary dashboard requests may create, activate, delete, or run live Plashboard templates and persistently change Plashboard state.

Mitigation: Install only where direct Plashboard administration is intended, and review requested dashboard changes before allowing the agent to execute destructive or activation actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with tool-oriented actions and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Plashboard tool calls that create, activate, delete, validate, or run dashboard templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
