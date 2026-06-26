## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs, plus access to 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuincyGunter](https://clawhub.ai/user/QuincyGunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call SkillBoss/HeyBoss APIs from an agent for Google Workspace-style automation and multi-provider AI model tasks, including chat, media generation, search, document processing, email, and SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes prompts, documents, audio, images, phone numbers, and other task data through a broad third-party AI/API gateway. <br>
Mitigation: Use a dedicated limited API key and submit confidential or sensitive data only after confirming the provider terms and internal data-handling requirements. <br>
Risk: The skill includes email, SMS, batch send, and remote download workflows that can affect external recipients or retrieve untrusted content. <br>
Mitigation: Require explicit user approval before sending email or SMS, running batch send actions, or downloading remote files. <br>
Risk: The Google Workspace framing may understate the breadth of non-Google AI and automation capabilities exposed by the skill. <br>
Mitigation: Review the full model and tool list before installation and use it only when a broad SkillBoss/HeyBoss gateway is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/QuincyGunter/gogs) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [HeyBoss API Base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
