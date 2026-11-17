## Description:

Helps agents break multi-step programming work into a visible todo checklist, keep only one item in progress, and mark each item complete as it is verified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to plan multi-step programming tasks, maintain a single active todo item, and verify each checklist item before closing the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad aliases may activate this skill during ordinary planning requests.

Mitigation: Use it for multi-step tasks where a visible checklist is useful, and disable or rename broad aliases if activation is too frequent.

Risk: The skill text is primarily Chinese, so non-Chinese users may receive planning guidance in an unexpected language.

Mitigation: Instruct the agent to match the user's language, or publish a localized variant for the intended audience.

Risk: Checklist workflow can add unnecessary process to simple one-step tasks.

Mitigation: Apply the skill only when tasks have three or more steps, multiple files, multiple phases, or evolving subtasks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaobod1/skills/huo15-todo)
- [Project homepage](https://github.com/zhaobod1/huo15-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown checklist and concise planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
