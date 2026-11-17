## Description:

三省吾身 - 深度自我审视与进化系统。基于角色理论、系统思维、认知偏差三大框架，通过五阶段闭环（反思→计划→执行→验证→固化）实现真正的自我进化。适用于任何需要深度反思的场景：项目复盘、工作改进、能力提升、习惯养成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[demo112](https://clawhub.ai/user/demo112)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers use this skill to guide structured self-reflection after project reviews, negative feedback, repeated mistakes, skill gaps, habit issues, or work-quality concerns. It helps produce reflection reports, improvement plans, execution records, verification reports, and durable checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can auto-start and steer a session into self-reflection without clear user intent.

Mitigation: Require explicit user invocation before activating the workflow.

Risk: The workflow can propose lasting updates to agent memory, skills, or shared workflow standards.

Mitigation: Review the exact path and diff before allowing edits to SOUL.md, SKILL.md, other skills, or shared workflow standards.

Risk: Reflection outputs can become misleading if proposed conclusions or action plans are accepted without review.

Mitigation: Review generated reports, plans, and checklists before using them to change behavior, documentation, or workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/demo112/skills/kuro-self-reflection)
- [README.en.md](artifact/README.en.md)
- [SKILL.md](artifact/SKILL.md)
- [Reflection report template](artifact/templates/reflection-report.md)
- [Optimization plan template](artifact/templates/optimization-plan.md)
- [Checklist template](artifact/templates/checklist.md)
- [Cognitive War Room example](artifact/examples/cognitive-war-room-case.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance, reports, plans, logs, verification summaries, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-oriented workflow with reusable markdown templates and optional durable workflow updates]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
