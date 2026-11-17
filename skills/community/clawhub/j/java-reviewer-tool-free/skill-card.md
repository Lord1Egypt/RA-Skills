## Description:

Java 代码变更审查工具，按 6 大维度生成结构化审查报告与修复建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Java developers and engineering teams use this skill to review git diffs or Java source files before submission. It identifies code quality, exception handling, security, performance, design, and resource-management issues, then returns severity-ranked findings and repair suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is broader in routing and capability text than its stated Java code review purpose, including unclear mutation-related authority.

Mitigation: Use it only for Java code review tasks and avoid granting write or deployment authority unless file modification is explicitly intended.

Risk: Generated fixes may be incorrect, incomplete, or inappropriate for the surrounding codebase.

Mitigation: Review and test generated changes before applying or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/java-reviewer-tool-free)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown review report with Java code blocks and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language interaction; generated fixes require review before application.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
