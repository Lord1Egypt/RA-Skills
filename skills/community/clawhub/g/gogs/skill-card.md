## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. And also 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to call SkillBoss/HeyBoss endpoints for chat, image, video, audio, web search, document processing, email, SMS, and related model workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is partly presented as a Google Workspace CLI while its artifact behavior is a broad third-party SkillBoss/HeyBoss AI gateway.

Mitigation: Install only when the intended use is broad SkillBoss/HeyBoss API access, and verify requested actions against the API endpoints before use.

Risk: Prompts, files, audio, phone numbers, OTP codes, and other inputs may leave the user's environment through third-party API calls.

Mitigation: Require explicit user approval before sending confidential, regulated, or personal data through the skill.

Risk: The skill includes email and SMS actions that can contact external recipients.

Mitigation: Confirm recipient, message content, and purpose with the user before invoking email or SMS operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quincygunter/skills/gogs)
- [SkillBoss Website](https://www.skillboss.co)
- [HeyBoss API Base URL](https://api.heybossai.com/v1)
- [Available Models Endpoint](https://api.heybossai.com/v1/models)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Video Models](artifact/video-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl/bash examples and JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated API calls]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
