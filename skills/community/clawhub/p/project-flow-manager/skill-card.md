## Description:

A project-flow management skill for structuring milestones, departments, schedules, KPI tracking, recurring reports, reminder drafts, and Markdown or HTML project boards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmywangjimmy](https://clawhub.ai/user/jimmywangjimmy)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, operations teams, and cross-functional contributors use this skill to create project records, add departments, milestones, and tasks, update progress, and generate status reports, reminder drafts, and visual boards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe project ID path handling may allow reads or writes outside the intended project folders.

Mitigation: Review commands before execution, use only trusted project IDs, and reject IDs containing slashes or '..'.

Risk: Generated reports, boards, project JSON, and email drafts may contain sensitive business information.

Mitigation: Use the skill only in trusted workspaces and review generated files before sharing or opening HTML output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmywangjimmy/skills/project-flow-manager)
- [Publisher profile](https://clawhub.ai/user/jimmywangjimmy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples and generated local JSON, Markdown, HTML, and text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local project data, report files, board files, and email reminder drafts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
