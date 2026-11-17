## Description:

面向个人的多岗位面试模拟工具，支持评分与改进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individual job seekers use this skill to run single-session interview simulations across engineering, product, business, and functional roles. It asks role- and seniority-adjusted questions, then returns per-question feedback, scores, a final scorecard, and study recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and write-capable tooling for an interview-practice workflow.

Mitigation: Review before installing and enable it only if command execution and write-capable tooling are acceptable for the environment.

Risk: The skill includes network diagnostics, secret-handling language, and generic data-operation claims that do not fit its stated interview-simulation purpose.

Mitigation: Limit use to interview simulation, avoid providing secrets, and prefer a version that removes those unrelated instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/interview-sim-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation with interview questions, per-question feedback, scoring, and a final scorecard.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ideal-answer guidance, module-level scores, hiring-style judgment, and learning recommendations.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
