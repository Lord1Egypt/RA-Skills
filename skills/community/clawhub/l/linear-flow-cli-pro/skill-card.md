## Description:

Linear流程CLI(专业版) helps agents and engineering teams automate Linear workflows with batch issue operations, dry-run previews, autonomy policies, Slack and ticket context intake, Git/JJ status updates, GraphQL query templates, webhook management, and cross-team initiative tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, Scrum Masters, DevOps engineers, and AI agent operators use this skill to plan and execute Linear task-management workflows. It is intended for batch migration, task triage, issue updates, webhook and notification setup, Git-linked status changes, and initiative or milestone coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad changes to Linear project data and integrations.

Mitigation: Use suggest-only or preview-required mode by default, and require dry-run review before write operations.

Risk: Linear workspace tokens may expose sensitive or business-critical data.

Mitigation: Restrict Linear tokens to the minimum required permissions and avoid exposing tokens in files, logs, prompts, or generated output.

Risk: Slack or ticket content may be converted into Linear issues with incorrect triage or sensitive details.

Mitigation: Review external context before applying triage, and verify team, priority, labels, and issue text before creation.

Risk: Autonomous mode, Git hooks, webhook changes, or bulk deletes can cause high-impact workspace changes.

Mitigation: Enable these capabilities only in controlled workspaces with trusted URLs, rollback procedures, and human approval for destructive actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, YAML, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Linear API or CLI actions that should be previewed before execution in sensitive workspaces.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
