## Description:

基于每日一练官网公开信息的中文 skill，帮助用户了解每日一练、判断是否适合自己的学习目标，并把任意主题转成可持续的每日训练方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitobook](https://clawhub.ai/user/aitobook)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and education-focused users use this skill to understand the 每日一练 product, choose a learning mode, and turn goals such as exam prep, subject study, or daily practice into small actionable training steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may provide the product's public site, login page, or WeChat contact when users ask how to access it.

Mitigation: Use only the official domains and contact details supplied in the artifact, and ask users to verify current access status on the official site.

Risk: The skill answers in Chinese by default, which may not match every user's preferred language.

Mitigation: Ask for or honor the user's preferred response language when the interaction context indicates a different language is needed.

Risk: Product status, pricing, or availability can change after the public information captured in the skill.

Mitigation: Avoid promising pricing or open registration, and direct users to the official site for current access details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aitobook/skills/meiriyilian)
- [每日一练 official site](https://www.meiriyilian.com)
- [每日一练 app](https://app.meiriyilian.com)
- [Overview reference](references/overview.md)
- [Learning modes reference](references/learning-modes.md)
- [Practice flow reference](references/practice-flow.md)
- [FAQ reference](references/faq.md)
- [Access reference](references/access.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Chinese Markdown guidance with concise practice plans and learning-mode recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers in Chinese by default and may include public product links or access guidance when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
