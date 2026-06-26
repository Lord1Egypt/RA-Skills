## Description: <br>
Provides SkillBoss API guidance for using 50+ models across chat, image, video, audio, search, document, email, SMS, and smart-routing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ModestyRichards](https://clawhub.ai/user/ModestyRichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to call SkillBoss-hosted models and utility actions from an agent using a single API key. It supports direct model calls and smart routing for generation, search, document processing, messaging, and related automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad actions through SkillBoss, including email, SMS, scraping, document, audio, and model-provider calls. <br>
Mitigation: Use a limited API key, monitor usage and billing, and enable the skill only when broad SkillBoss access is intended. <br>
Risk: Messaging, OTP, scraping, batch messaging, and smart-routed provider actions can affect external services or people. <br>
Mitigation: Require explicit human approval before executing those actions. <br>
Risk: Sensitive files, audio, or documents may be sent to external processing providers. <br>
Mitigation: Avoid processing sensitive inputs unless approved for the relevant provider and workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ModestyRichards/proactive-agent-hub) <br>
- [Publisher profile](https://clawhub.ai/user/ModestyRichards) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and can produce external API requests through SkillBoss.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
