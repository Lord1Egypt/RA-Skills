## Description:

实现计划生成 - 从需求生成多阶段实施计划：基础→逻辑→接口→测试→部署。含模板、依赖分析、验收标准

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to turn requirements into staged implementation plans with dependencies, effort estimates, risks, acceptance criteria, and Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic planning trigger words may activate the skill when the user did not intend to use it.

Mitigation: Confirm that the user wants an implementation plan before applying the template when the request is ambiguous.

Risk: Generated plans can contain inaccurate dependencies, effort estimates, or acceptance criteria.

Mitigation: Review generated plans against project requirements and adjust estimates, dependencies, and risks before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-write-plan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with structured implementation phases and optional Python planning code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include phase dependencies, effort estimates, acceptance criteria, risk notes, and plan templates.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
