## Description: <br>
Relationship intelligence for OpenClaw that detects outreach signals, scores and ranks opportunities, and prepares multilingual tone-aware drafts while requiring final user approval before anything is sent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abderrahman-Jalled](https://clawhub.ai/user/Abderrahman-Jalled) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to identify timely personal and professional outreach opportunities, rank them by evidence and appropriateness, and draft messages in an appropriate channel, tone, and language. It is intended for relationship maintenance, not sales pipelines, lead generation, or CRM data entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill normalizes using private communication history and inferred cultural or language attributes without clear consent or override controls. <br>
Mitigation: Use it only with contacts and data sources intentionally provided by the user, and verify inferred language or cultural cues before drafting. <br>
Risk: Outreach drafts may include sensitive relationship, health, financial, legal, or life-event context if the user provides that information. <br>
Mitigation: Keep drafts limited to evidence the user has supplied, avoid sensitive details unless explicitly instructed, and require user review before any message is sent. <br>
Risk: The skill may over-personalize messages by mixing work and personal context. <br>
Mitigation: Keep work and personal streams separate unless the user explicitly asks to combine them. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/Abderrahman-Jalled/improve-relationships) <br>
- [Digest template](artifact/templates/digest.md) <br>
- [Personal outreach templates](artifact/templates/outreach_personal.md) <br>
- [Professional outreach templates](artifact/templates/outreach_professional.md) <br>
- [Ritual and cultural occasion templates](artifact/templates/rituals.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Text] <br>
**Output Format:** [Markdown digests and draft outreach messages with evidence, channel, language, tone, score, and approval action fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only output; the skill states that messages require final user approval and are not sent automatically.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
