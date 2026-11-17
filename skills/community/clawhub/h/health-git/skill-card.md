## Description:

Health Git helps an agent apply a Git-like workflow to health tracking by logging care commits, opening intervention-plan PRs, supporting review, and auditing events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erinyu](https://clawhub.ai/user/erinyu)

### License/Terms of Use:


## Use Case:

Consumers, health coaches, doctors, and data analysts use this skill to record health check-ins, submit and review intervention plans, inspect safety rules, and audit outcomes in a local health workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health workflow data while the security evidence says authentication is off by default.

Mitigation: Enable authentication before using real health data, replace example API keys, and require explicit user confirmation before submitting health data.

Risk: Medication-related safety rules can be updated through the documented workflow.

Mitigation: Restrict rule updates to authorized administrators or reviewers and require explicit confirmation for medication-related changes.

Risk: The security evidence reports an unaudited runtime and incomplete server-code review context.

Mitigation: Install only in a trusted development environment unless the complete server code and dependency manifest are supplied and reviewed.

## Reference(s):

- [Health Git on ClawHub](https://clawhub.ai/erinyu/skills/health-git)
- [Publisher profile: erinyu](https://clawhub.ai/user/erinyu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable local Health Git service before API examples can execute.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
