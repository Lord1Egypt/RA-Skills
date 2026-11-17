## Description:

面向 3-7 岁幼儿的 L1-L4 思维启蒙体系，生成 A4 可打印训练页与答案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT

## Use Case:

Parents, teachers, and agent users use this skill to generate printable thinking and logic worksheets for children ages 3-7, diagnose starting level, review answers, and plan targeted follow-up practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated worksheets, answer files, roster outputs, and progress notes may contain child names, IDs, scores, or other personal learning data.

Mitigation: Use --no-name or pseudonyms for class rosters, avoid unnecessary personal details, and store generated files only in appropriate local workspaces.

Risk: Generated _summary.csv files may expose roster data and require caution until CSV escaping or formula neutralization is fixed.

Mitigation: Review CSV summaries before sharing or opening them in spreadsheet tools, and avoid putting formula-like values in roster fields.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liyumingben/skills/kindergarten-thinking-course)
- [SkillHub Listing](https://skillhub.cn/skills/user_89a2cacc/kindergarten-thinking-course)
- [Activity Specification](references/activity-spec.md)
- [Curriculum](references/curriculum.md)
- [Pedagogy](references/pedagogy.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Printable HTML worksheets, answer JSON, Markdown guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated answer JSON records level, seed, topics, activities, and answers for grading, review, and regeneration.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
