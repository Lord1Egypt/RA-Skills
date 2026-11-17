## Description:

Pub Mcporter guides agents in using the mcporter and SkillBoss API to list models, configure authentication, and call AI, search, document, email, and SMS capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to discover available SkillBoss models, configure SKILLBOSS_API_KEY authentication, and prepare API calls for chat, media generation, search, document processing, email, SMS, and related utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, documents, audio, images, phone numbers, and messages may be sent to SkillBoss/HeyBossAI and downstream providers.

Mitigation: Use the skill only when the publisher and service are trusted, and avoid sending sensitive inputs unless the user explicitly approves the disclosure.

Risk: Email, SMS, and OTP actions can contact external recipients.

Mitigation: Require explicit user approval for the recipient, content, and action before preparing or running any email, SMS, OTP, or notification request.

Risk: Smart routing can automatically select a provider for a task.

Mitigation: Use direct model IDs when provider choice, data handling, cost, or compliance requirements matter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/mcporters)
- [Publisher Profile](https://clawhub.ai/user/modestyrichards)
- [SkillBoss Website](https://www.skillboss.co)
- [HeyBossAI API Base](https://api.heybossai.com/v1)
- [Audio Models](audio-models.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Search and Scraping Models](search-models.md)
- [Tool Models](tools-models.md)
- [Video Models](video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, curl commands, and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; prepared requests may return text, JSON, URLs, files, or communication results depending on the selected model.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
