## Description: <br>
Pub Pdf gives agents PDF and document-processing guidance plus SkillBoss API examples for chat, media generation, search, scraping, email, SMS, and related model calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlvisDunlop](https://clawhub.ai/user/AlvisDunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to invoke SkillBoss endpoints for PDF/document processing and multimodal model tasks through a shared API key. It is most appropriate when broad external API access for model routing, document parsing, media generation, search, and communications is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release presents as PDF tooling but grants broad access to an external SkillBoss API gateway. <br>
Mitigation: Install only when broad SkillBoss API access is intended, use a limited API key with spending controls, and review requested actions before execution. <br>
Risk: Document upload or parsing can expose sensitive files to external processing. <br>
Mitigation: Avoid sensitive documents unless external processing is acceptable for the use case and approval path. <br>
Risk: Email, SMS, OTP, batch messaging, scraping, and document-upload actions can affect third parties or external systems. <br>
Mitigation: Require explicit user approval before those actions and limit the API key to the smallest practical permission set. <br>


## Reference(s): <br>
- [ClawHub Pub Pdf Release](https://clawhub.ai/AlvisDunlop/pdfs) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [SkillBoss API Base](https://api.heybossai.com/v1) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search and Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; API responses vary by selected model and provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
