## Description:

Ruiguan Text Trademark Detection checks e-commerce product titles and listing text against supported regional trademark data and returns match details, risk scores, and review guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and listing operators use this skill to screen product titles, descriptions, bullet points, and keywords for possible text trademark conflicts before publishing listings. It supports risk-first review across the skill's listed marketplace regions but does not provide legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product listing text and authentication data are sent to LinkFox services.

Mitigation: Use the skill only for data appropriate to share with LinkFox and keep API keys out of shared prompts, logs, and shell history.

Risk: The skill can persist full API responses and cache files locally.

Mitigation: Review and periodically clean the generated linkfox response and cache directories, especially after scanning sensitive listing drafts.

Risk: Endpoint override environment variables and built-in billing flows can change where requests go or trigger account/payment actions.

Mitigation: Avoid endpoint overrides unless intentionally testing, and review billing actions before running onboarding payment commands.

Risk: Trademark matches and risk scores are screening aids, not legal clearance.

Mitigation: Use results for preliminary review and consult an IP attorney for definitive trademark decisions.

## Reference(s):

- [睿观-文本商标检测 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-ruiguan-text-trademark-detection)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with tables and optional JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are persisted as JSON; larger responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
