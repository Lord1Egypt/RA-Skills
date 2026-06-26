## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli, with access to 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlvisDunlop](https://clawhub.ai/user/AlvisDunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to work with Markdown-based Obsidian vaults and call SkillBoss-hosted AI, search, document, email, SMS, and media models through API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad SkillBoss API access, including email, SMS, document, search, and media-processing actions. <br>
Mitigation: Use a restricted or low-spend API key where possible and require explicit approval before email, SMS, OTP, batch message, document upload, or media upload actions. <br>
Risk: Private vault contents or regulated data could be sent to external providers through model, document, search, or media requests. <br>
Mitigation: Avoid sending sensitive notes or regulated data unless the provider and downstream processing are approved for that data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AlvisDunlop/obsidians) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, and model reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls; API responses may include generated text, URLs, files, or structured data depending on the selected model.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
