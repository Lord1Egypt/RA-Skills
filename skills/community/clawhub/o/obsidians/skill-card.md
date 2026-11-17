## Description:

Pub Obsidian guides agents through Obsidian-vault Markdown workflows and SkillBoss API calls for chat, media generation, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Markdown note vaults and call SkillBoss models for chat, image generation, video generation, audio, web search, document parsing, email, SMS, and related tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is named for Obsidian but mainly instructs the agent to use a broad third-party SkillBoss API that can send user content externally.

Mitigation: Review planned API calls before execution and avoid sending private vault notes, documents, audio, images, email addresses, or phone numbers unless the user explicitly intends to share that data with SkillBoss.

Risk: The skill includes email, SMS, and OTP-related actions through the SkillBoss API.

Mitigation: Require explicit user confirmation before sending email, SMS, notifications, or OTP requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/obsidians)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss models endpoint](https://api.heybossai.com/v1/models)
- [SkillBoss website](https://www.skillboss.co)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for SkillBoss API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
