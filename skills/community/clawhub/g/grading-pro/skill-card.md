## Description:

文科主观题智能批改评分系统，支持初高中英语写作、语文作文和语文阅读理解评分标准，用于生成评分、错误分析、改进建议和优化范文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[makiwinster72](https://clawhub.ai/user/makiwinster72)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, tutors, and education-focused agents use this skill to grade junior and senior middle-school Chinese and English subjective assignments against local rubric JSON files, then produce scoring reports, error analysis, improvement suggestions, and polished sample answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved rubric changes can affect later grading results.

Mitigation: Review proposed criteria/*.json updates before persisting them and keep educator-approved rubric versions.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Rubric Criteria](artifact/criteria/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown grading report with scores, annotated feedback, recommendations, and revised sample answer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference and propose updates to local criteria/*.json rubric files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
