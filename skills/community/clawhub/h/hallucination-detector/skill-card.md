## Description:

幻觉检测器 - 原创技能。检测AI生成代码中的幻觉内容，包括不存在的API、错误的参数、虚假引用等。适用于代码审查、AI编程辅助、质量保证等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to check AI-generated code for hallucinated APIs, incorrect parameters, false references, incompatible versions, type errors, and contradictory logic before accepting or executing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill trigger terms overlap with ordinary code review requests, so it may be invoked when a general review was intended.

Mitigation: Invoke it explicitly when hallucination checks are needed and pair its findings with normal code review judgment.

Risk: The artifact describes review heuristics rather than an executable verifier, so findings may miss project-specific APIs or version constraints.

Mitigation: Confirm reported issues against the target project's dependencies, documentation, type checker, tests, or package registry before making changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with findings, confidence estimates, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or installation steps are included in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
