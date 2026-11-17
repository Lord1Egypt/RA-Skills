## Description:

Provides Chinese-language explanations of places and images through Migu's AI guide service, with support for follow-up questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llforest](https://clawhub.ai/user/llforest)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request Chinese-language descriptions of cities, attractions, or selected images and ask follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The user-provided Migu JWT can grant access to the user's account if exposed.

Mitigation: Treat the JWT like a password, keep it out of chats and screenshots, restrict access to its saved file, and delete or rotate it when finished.

Risk: Questions and selected images are sent to the Migu service.

Mitigation: Share only content intended for that service; do not upload private images without the user's consent.

## Reference(s):

- [Migu AI Guide ClawHub release](https://clawhub.ai/llforest/skills/migu-ai-guide)
- [Migu travel guide service](https://gulangyu.migudm.cn/multi-city-trip-agent/)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Chinese-language guide text, optionally returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports continued conversations using a saved session ID.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
