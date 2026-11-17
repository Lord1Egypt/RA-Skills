## Description:

Pub Himalaya helps agents use SkillBoss API examples to manage email workflows and call AI models for chat, image, video, audio, search, document processing, email, and SMS tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to draft and run SkillBoss API calls for model access, document processing, web search, and communication workflows. It is most relevant when an agent needs concise bash or curl guidance for SkillBoss-backed services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External API calls may send documents, private URLs, email content, recipient addresses, phone numbers, audio, or images to SkillBoss-backed services.

Mitigation: Review sensitive inputs before submission and require explicit user approval before sending private data to external services.

Risk: Email and SMS capabilities can contact third parties or trigger verification workflows.

Mitigation: Confirm recipients, phone numbers, message content, and user intent before sending email or SMS requests.

Risk: The security summary reports confusing identity and scope for the skill.

Mitigation: Verify the intended SkillBoss API endpoint, requested operation, and required API key before using the generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/himalaya-tool)
- [Publisher profile](https://clawhub.ai/user/godferylindsay)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss website](https://www.skillboss.co)
- [Chat models](artifact/chat-models.md)
- [Image models](artifact/image-models.md)
- [Audio models](artifact/audio-models.md)
- [Search and scraping models](artifact/search-models.md)
- [Tool models](artifact/tools-models.md)
- [Video models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
