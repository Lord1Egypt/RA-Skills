## Description: <br>
Pub Himalaya provides command examples for using the SkillBoss API to manage email and route requests to AI models for chat, media generation, speech, search, document processing, SMS, and related tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodferyLindsay](https://clawhub.ai/user/GodferyLindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill as API guidance for invoking SkillBoss-hosted models and utility services, including email, search, document parsing, media generation, speech, SMS verification, embeddings, and presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive prompts, files, document URLs, email contents, recipient addresses, phone numbers, and OTP-related data may be sent to SkillBoss or api.heybossai.com. <br>
Mitigation: Use a limited API key, avoid real mailbox or identity-verification data unless the provider is trusted for the use case, and redact sensitive inputs where possible. <br>
Risk: The release is branded as an email CLI, but the artifact primarily documents calls to a third-party AI API. <br>
Mitigation: Treat it as third-party API guidance, review each generated command before execution, and confirm data handling expectations before connecting production email or SMS workflows. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/GodferyLindsay/himalaya-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/GodferyLindsay) <br>
- [SkillBoss API Base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss Site](https://www.skillboss.co) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search and Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
