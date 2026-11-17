## Description:

Automates PingCode timesheet filling by creating work items, setting task properties, and logging hours from manual task lists or Git commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers who track work in PingCode use this skill to create task and sub-task structures, set dates and states, and log work hours after reviewing and confirming the proposed plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live PingCode session cookies and optional Git tokens.

Mitigation: Store cookies and tokens with restrictive permissions, export only necessary cookies, prefer least-privilege short-lived Git tokens, and verify the configured PingCode and Git hosts before use.

Risk: The skill can create PingCode work items and register hours in a live account.

Mitigation: Use it only where automated work-item creation and hour logging are acceptable, and execute only after reviewing and explicitly confirming the proposed task and hour plan.

## Reference(s):

- [PingCode TimeLogger on ClawHub](https://clawhub.ai/huuuwnnn-droid/skills/pingcode-timelogger)
- [PingCode Work Category IDs](references/category-ids.md)
- [PingCode TimeLogger Configuration](references/config-template.yaml)
- [Git Integration for PingCode TimeLogger](references/git-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with YAML configuration snippets, API request details, and progress/status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before creating work items or logging hours.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
