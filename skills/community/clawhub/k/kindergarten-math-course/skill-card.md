## Description:

为 3-7 岁幼儿生成 L1-L5 识数、比较、分解组成和 20 以内加减法练习页，并提供诊断、批改反馈与进阶建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT

## Use Case:

Parents, caregivers, and educators use this skill to create printable kindergarten math worksheets, diagnose a child's current level, grade returned answers, and choose focused follow-up practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated worksheet HTML can include unescaped user-provided titles, names, or review values, which may run active browser content if malicious text is supplied.

Mitigation: Use only trusted worksheet titles, child names, and wrong-question values, and avoid pasting copied web content or third-party messages into those fields until dynamic text is HTML-escaped.

## Reference(s):

- [课程体系](references/curriculum.md)
- [教学法与家长指导话术](references/pedagogy.md)
- [练习页生成规范](references/worksheet-spec.md)
- [ClawHub skill page](https://clawhub.ai/liyumingben/skills/kindergarten-math-course)
- [ClawDis homepage](https://skillhub.cn/skills/user_89a2cacc/kindergarten-math-course)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Printable HTML worksheets, JSON answer files, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Worksheet generation can include level, topic, count, seed, name, layout columns, diagnostic preset, and review inputs.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
