## Description:

Provides Bash examples for using the SkillBoss/HeyBossAI API to access chat, media generation, search, scraping, document, email, and SMS capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to discover and call SkillBoss/HeyBossAI models and utility endpoints from shell commands, including chat, generated media, web search, document processing, email, and SMS workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route prompts, documents, media, repository context, contact details, or other sensitive data to a third-party API.

Mitigation: Review intended data flows before use and avoid sending secrets, private repository data, personal documents, audio, images, email content, or phone numbers unless third-party processing is approved.

Risk: Email, batch email, SMS, and OTP examples can cause external communications or verification side effects.

Mitigation: Require explicit user confirmation before any email, batch email, SMS, or OTP action.

Risk: The GitHub-oriented name and description may understate that the artifact mainly documents SkillBoss/HeyBossAI API usage.

Mitigation: Install only when broad SkillBoss/HeyBossAI API access is intended, and review the artifact contents before enabling it for an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/github-ai)
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca)
- [SkillBoss website](https://www.skillboss.co)
- [HeyBossAI API base URL](https://api.heybossai.com/v1)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
