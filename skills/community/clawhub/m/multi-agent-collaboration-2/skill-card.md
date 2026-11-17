## Description:

This skill guides human-supervised multi-agent collaboration by helping an orchestrating AI clarify requirements, decompose work into atomic tasks, review agent outputs, and keep the human owner responsible for direction and acceptance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allin-zhang](https://clawhub.ai/user/allin-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product managers, independent developers, small teams, and creators use this skill to turn vague product, content, code, or MVP work into bounded multi-agent workflows with explicit planning, execution, review, and human acceptance steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a Chinese-language workflow guide, so users who do not read Chinese may misunderstand task boundaries or review steps.

Mitigation: Ask the agent to translate outputs or explicitly follow the user's preferred language before applying the workflow.

Risk: Agent-generated task plans or reviews can still contain incorrect guidance or miss risks in the actual project.

Mitigation: Keep human confirmation at planning, review, and final acceptance steps, and run project-specific checks before accepting work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/allin-zhang/skills/multi-agent-collaboration-2)
- [Atomic Task Template](references/task-template.md)
- [Review Checklist](references/review-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, structured task blocks, review tables, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default response language is Chinese; outputs emphasize bounded task scope, reviewability, and human acceptance.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
