## Description: <br>
Pub Mcporter helps agents use the mcporter CLI and SkillBoss API to list, configure, authenticate, and call MCP servers, tools, and 50+ model capabilities across chat, media generation, search, documents, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ModestyRichards](https://clawhub.ai/user/ModestyRichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to discover SkillBoss-backed models, construct authenticated API calls, and run tasks such as chat, media generation, web search, document parsing, email, and SMS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, documents, media, email, and SMS-related content to external SkillBoss APIs. <br>
Mitigation: Use it only with data approved for SkillBoss, protect the SKILLBOSS_API_KEY, and revoke the key if exposure is suspected. <br>
Risk: Email, SMS, OTP, document, media, or sensitive prompt requests can affect third parties or expose private information. <br>
Mitigation: Require the agent to show the exact destination, content, and request payload, then obtain explicit approval before execution. <br>
Risk: Smart routing can choose providers automatically, which may reduce visibility into where a request is handled. <br>
Mitigation: Use explicit model IDs for sensitive workloads and review request payloads before sending them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ModestyRichards/mcporters) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base](https://api.heybossai.com/v1) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline cURL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated SkillBoss API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
