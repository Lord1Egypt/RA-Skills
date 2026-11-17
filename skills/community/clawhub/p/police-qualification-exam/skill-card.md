## Description:

警察执法资格考试助手 provides outline review, historical question data, high-frequency topic analysis, mock practice, and study-planning support for police law-enforcement qualification exam preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webpenbot](https://clawhub.ai/user/webpenbot)

### License/Terms of Use:

MIT-0

## Use Case:

Exam candidates, trainers, and agents supporting Chinese police law-enforcement qualification exam preparation use this skill to review the 2026 outline, search curated question data, analyze common topics, generate practice prompts, and create study plans.

### Deployment Geography for Use:

Global; content is specific to China's police law-enforcement qualification exam.

## Known Risks and Mitigations:

Risk: The optional web helper can fetch arbitrary user-supplied URLs from the user's machine.

Mitigation: Restrict it to trusted public WeChat or exam domains, or disable it in sensitive environments.

Risk: Exam and legal study outputs may be outdated or inconsistent with official materials.

Mitigation: Treat outputs as study aids and verify outlines, laws, answers, and procedures against official sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webpenbot/skills/police-qualification-exam)
- [Artifact README](artifact/README.md)
- [Usage examples](artifact/examples/usage_examples.md)
- [2026 exam outline data](artifact/data/exam_outline_2026.json)
- [Knowledge points data](artifact/data/knowledge_points.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown-style Chinese study guidance, exam summaries, question explanations, and occasional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled local JSON exam-outline, knowledge-point, and historical-question data; optional web article fetching should be controlled by the host environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
