## Description:

智能课堂 turns a teaching topic, course material, or objective into a ready-to-teach interactive classroom package with lesson flow, slides, activities, formative quizzes, AI teacher and peer roles, and follow-up practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuhaolong123456](https://clawhub.ai/user/xuhaolong123456)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, curriculum designers, and classroom-support agents use this skill to convert topics, source materials, or objectives into structured interactive lesson packages, delivered in Chinese by default. It is suited for lesson planning, slide outlines, classroom activities, formative quizzes, differentiated support, and validated lesson JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide real student private data, sensitive grades, credentials, or other protected classroom information.

Mitigation: Avoid collecting or pasting real student private data or credentials; use fictional or anonymized examples for lesson design and feedback.

Risk: Generated lessons for child safety, mental health, medical, legal, or other high-risk topics may be incomplete or inappropriate for the audience.

Mitigation: Treat such content as general educational support and have a qualified teacher verify age appropriateness and authoritative sources before classroom use.

Risk: The bundled JSON validator is a convenience checker rather than a hardened service for untrusted bulk input.

Mitigation: Run the validator locally on expected lesson JSON files and do not expose it as a security boundary or untrusted bulk-processing service.

Risk: Lesson plans can contain unsupported factual claims or unclear distinctions between user-provided material and supplemental content.

Mitigation: Review factual content, verify cited or uncertain points against trusted sources, and clearly separate source material from added explanation.

## Reference(s):

- [Classroom package JSON schema](references/lesson-schema.md)
- [ClawHub skill page](https://clawhub.ai/xuhaolong123456/skills/openmaic-classroom)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown lesson plan plus lesson.json-compatible JSON; optional shell command guidance for local validation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a human-readable lesson.md and a lesson.json package conforming to the bundled classroom schema.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
