## Description: <br>
Provides Markdown conversion guidance for documents and a broad SkillBoss API gateway for AI models, search, scraping, email, SMS, and media generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KirkRaman](https://clawhub.ai/user/KirkRaman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to draft API calls for document-to-Markdown conversion and to route AI, search, scraping, email, SMS, and media-generation requests through SkillBoss/HeyBossAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a broad third-party AI and service gateway under a Markdown-converter name. <br>
Mitigation: Install it only when that broader SkillBoss/HeyBossAI access is intended, and review generated commands before use. <br>
Risk: API calls may transmit sensitive documents, recordings, email content, phone numbers, prompts, or generated media to external services. <br>
Mitigation: Avoid sensitive inputs unless the external data flow is approved, and use a dedicated low-privilege SKILLBOSS_API_KEY where possible. <br>
Risk: Email and SMS capabilities can cause real-world communications or verification messages. <br>
Mitigation: Require explicit human review before executing email or SMS commands, especially batch or notification flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KirkRaman/markdown-converters) <br>
- [KirkRaman ClawHub profile](https://clawhub.ai/user/KirkRaman) <br>
- [HeyBossAI API](https://api.heybossai.com/v1) <br>
- [HeyBossAI models endpoint](https://api.heybossai.com/v1/models) <br>
- [SkillBoss](https://www.skillboss.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
