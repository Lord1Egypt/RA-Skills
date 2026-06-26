## Description: <br>
Helps agents rewrite text to sound more natural while also documenting SkillBoss API calls for chat, media generation, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbelTennyson](https://clawhub.ai/user/AbelTennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to make generated text sound more natural and to call SkillBoss-hosted models for chat, images, video, audio, search, scraping, document processing, email, and SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised text-humanizing purpose does not fully match the artifact surface, which includes broad external API, scraping, email, and SMS/OTP capabilities. <br>
Mitigation: Install only when a broad external API broker is intended, and review the full artifact capability surface before use. <br>
Risk: Text, files, audio, search targets, emails, or phone numbers may be sent to external providers through SkillBoss-routed model calls. <br>
Mitigation: Confirm which provider receives each payload and avoid sensitive documents, credentials, or regulated data unless data handling is clear. <br>
Risk: Email and SMS actions can contact third parties. <br>
Mitigation: Require explicit user approval before sending any email, SMS, or OTP request. <br>


## Reference(s): <br>
- [Pub Humanizer release page](https://clawhub.ai/AbelTennyson/humanizers) <br>
- [SkillBoss API key page](https://www.skillboss.co) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with curl examples and model reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
