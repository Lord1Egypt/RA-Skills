## Description:

Generates structured learning plans with staged milestones, daily or weekly tasks, recommended resources, and progress checkpoints for study goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huajianjiu000](https://clawhub.ai/user/huajianjiu000)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and agents use this skill to turn a goal, current level, time budget, and learning mode into a staged study plan. It is most directly suited to Chinese-language learning-plan requests, including programming, exam preparation, language learning, and general skill development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese trigger phrases may activate the skill for general study questions.

Mitigation: Use the skill when the user clearly asks for a study plan, learning path, or exam preparation plan, and confirm intent when the request is ambiguous.

Risk: The bundled templates are Chinese-only unless the agent adapts them.

Mitigation: Translate or localize the generated plan when the user requests another language.

## Reference(s):

- [Learning Plan Templates](artifact/references/plan_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown study plan with tables, task lists, resource suggestions, and evaluation checkpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shell commands or Python code when the agent uses the bundled local example script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
