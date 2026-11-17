## Description:

A Chinese-language skill that lets an agent switch and sustain its conversational style according to user-selected MBTI types, including single-type, comparison, mixed-style, recommendation, and reset flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuetsui](https://clawhub.ai/user/fuetsui)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent to answer in a specific MBTI-inspired conversation style, compare two styles, blend compatible styles, or return to the default assistant tone. The skill is focused on expression, structure, pacing, and question style rather than personality testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MBTI labels may be mistaken for personality diagnosis or may produce stereotyped phrasing.

Mitigation: Use the skill as an expression-layer style control and keep task quality, accuracy, and non-stereotyped language ahead of persona effects.

Risk: The bundled maintenance script contains developer-local paths and should not be run casually.

Mitigation: Treat the script as maintainer evidence only; remove or parameterize local paths before using it to regenerate reference files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuetsui/skills/my-mbti)
- [MyMBTI Reference Index](references/index.md)
- [INTJ Style Card](references/INTJ.md)
- [INTP Style Card](references/INTP.md)
- [ENTJ Style Card](references/ENTJ.md)
- [ENTP Style Card](references/ENTP.md)
- [INFJ Style Card](references/INFJ.md)
- [INFP Style Card](references/INFP.md)
- [ENFJ Style Card](references/ENFJ.md)
- [ENFP Style Card](references/ENFP.md)
- [ISTJ Style Card](references/ISTJ.md)
- [ISFJ Style Card](references/ISFJ.md)
- [ESTJ Style Card](references/ESTJ.md)
- [ESFJ Style Card](references/ESFJ.md)
- [ISTP Style Card](references/ISTP.md)
- [ISFP Style Card](references/ISFP.md)
- [ESTP Style Card](references/ESTP.md)
- [ESFP Style Card](references/ESFP.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain a user-selected MBTI style across turns until the user switches style or resets to the default tone.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
