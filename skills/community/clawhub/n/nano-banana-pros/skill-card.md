## Description: <br>
Pub Banana helps agents generate and edit images with Nano Banana Pro and access SkillBoss-hosted models for chat, audio, video, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TobeyRebecca](https://clawhub.ai/user/TobeyRebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call SkillBoss models through a shared API key for image generation and editing, multimodal generation, search, document parsing, messaging, and model-routing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single SkillBoss API key grants broad access to model, scraping, email, and SMS actions. <br>
Mitigation: Use a separate or least-privilege API key when possible and require explicit approval before high-impact actions. <br>
Risk: Prompts, files, URLs, or message content may be routed to external SkillBoss and downstream model providers. <br>
Mitigation: Avoid secrets or regulated data unless the user has approved the provider path and data handling requirements. <br>
Risk: Email, SMS, OTP, and batch messaging actions can contact real recipients. <br>
Mitigation: Confirm recipients, content, purpose, and authorization before sending any message or verification request. <br>
Risk: Web scraping and document-processing actions can retrieve or transform third-party or sensitive content. <br>
Mitigation: Confirm the source URL or document is appropriate to process and review generated outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TobeyRebecca/nano-banana-pros) <br>
- [Publisher Profile](https://clawhub.ai/user/TobeyRebecca) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [SkillBoss API Base](https://api.heybossai.com/v1) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Audio Models](audio-models.md) <br>
- [Video Models](video-models.md) <br>
- [Search and Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated media URLs, downloaded media files, parsed documents, messages, or model responses depending on the selected SkillBoss model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
