## Description:

Generate and edit images with Nano Banana Pro (Gemini 3 Pro Image) and access SkillBoss models for image, video, audio, chat, search, document processing, email, and SMS tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call SkillBoss/HeyBoss model APIs for media generation, chat, search, document parsing, and messaging workflows through agent-proposed API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, URLs, audio, recipient addresses, and phone numbers may be sent to SkillBoss/HeyBossAI and downstream model or tool providers.

Mitigation: Install only when the user trusts those services with the data being processed, and avoid private or regulated data unless the deployment has appropriate approvals.

Risk: Email, SMS, document parsing, scraping, and media-processing actions can have high impact or expose sensitive information.

Mitigation: Require explicit user approval before running these actions, especially when they involve external recipients, phone numbers, private documents, or third-party websites.

Risk: Broad model routing and live model discovery can change which provider processes a task.

Mitigation: Prefer explicit model IDs for sensitive workflows and review the selected model or route before sending data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/nano-banana-pros)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Skill instructions](artifact/SKILL.md)
- [Audio model catalog](artifact/audio-models.md)
- [Chat model catalog](artifact/chat-models.md)
- [Image model catalog](artifact/image-models.md)
- [Search and scraping model catalog](artifact/search-models.md)
- [Tool model catalog](artifact/tools-models.md)
- [Video model catalog](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash curl examples and API request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; API results may include generated media URLs, text responses, parsed document markdown, email or SMS actions, and downloaded files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
