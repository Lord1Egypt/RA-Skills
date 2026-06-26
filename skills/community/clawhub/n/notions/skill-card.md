## Description: <br>
Provides bash-oriented guidance for using SkillBoss as a broad API gateway for chat, image, video, audio, search, scraping, document processing, email, SMS, and Notion-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ModestyRichards](https://clawhub.ai/user/ModestyRichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover SkillBoss models and draft shell commands for model inference, media generation, search, document processing, and outbound messaging. Reviewers should treat it as a broad SkillBoss API gateway rather than a narrow Notion integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill name and listing imply a Notion-focused tool, while the evidence describes a broad SkillBoss API gateway. <br>
Mitigation: Install it only when the intended use includes broad model, search, document, and messaging access; do not approve it as a narrow Notion-only skill. <br>
Risk: The skill can route prompts, documents, URLs, and generated media requests through third-party services. <br>
Mitigation: Use restricted API keys and avoid sending sensitive documents, private URLs, or regulated data unless the downstream provider data flow is approved. <br>
Risk: The skill includes email, SMS, scraping, and document-processing actions that may create external side effects. <br>
Mitigation: Require explicit human review before executing email, SMS, scraping, or document-processing commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ModestyRichards/notions) <br>
- [Publisher profile](https://clawhub.ai/user/ModestyRichards) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Chat model list](artifact/chat-models.md) <br>
- [Image model list](artifact/image-models.md) <br>
- [Video model list](artifact/video-models.md) <br>
- [Audio model list](artifact/audio-models.md) <br>
- [Search and scraping model list](artifact/search-models.md) <br>
- [Tool model list](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include API calls that invoke third-party models or outbound messaging services when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
