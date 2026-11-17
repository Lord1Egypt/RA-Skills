## Description:

数学公式计算专家 - Excel 公式解析、分步计算、边界验证。专用于招投标价格分计算、复杂公式求解。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gipsy12](https://clawhub.ai/user/gipsy12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and procurement teams use this skill to parse Excel formulas, calculate bid evaluation price scores step by step, and check boundary conditions such as division by zero, negative scores, and overflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses a mutable latest package reference.

Mitigation: Verify the ClawHub package and publisher before installation and prefer a pinned installer version when available.

Risk: Sensitive formulas or bid data could be retained if local learning notes are enabled.

Mitigation: Only allow LEARNINGS.md updates when local storage of those notes is acceptable for the data being processed.

Risk: Incorrect formula interpretation or arithmetic could affect procurement scoring decisions.

Mitigation: Require users to confirm formula structure, inputs, units, and final calculations before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gipsy12/skills/math-formula-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with formulas, tables, and step-by-step calculations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Excel formulas, arithmetic traces, validation notes, and concise recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
