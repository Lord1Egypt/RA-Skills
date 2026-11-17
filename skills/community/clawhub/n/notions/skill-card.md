## Description:

Provides SkillBoss API usage guidance for Notion-labeled workflows and a broad set of model, search, document, email, and SMS actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to guide an agent in calling SkillBoss APIs for chat, media generation, search, document parsing, email, SMS, and related model routing tasks. Reviewers should treat it as a broad API gateway skill rather than a Notion-only integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill is labeled as Notion but actually teaches broad SkillBoss API use, including email, SMS, scraping, and AI model calls.

Mitigation: Review and approve it as a broad SkillBoss/API gateway skill, not as a narrow Notion integration.

Risk: The server security guidance says the skill can send selected data to api.heybossai.com and potentially use provider models, scraping, email, and SMS actions.

Mitigation: Install only when that data flow is intended, and require explicit user approval before email, SMS, scraping, document upload, or cost-incurring model calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/notions)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss website](https://www.skillboss.co)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Video Models](artifact/video-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends API requests to https://api.heybossai.com/v1.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
