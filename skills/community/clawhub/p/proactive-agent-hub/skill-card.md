## Description:

Pub Proactive helps agents use SkillBoss as a unified API gateway for proactive assistance and 50+ models across chat, image, video, audio, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to discover and call SkillBoss models from an agent workflow, including generation, search, document processing, and communication tasks through a single API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, documents, recordings, contacts, email content, SMS targets, and account data to SkillBoss or downstream providers.

Mitigation: Do not use private or sensitive data unless the user has approved that transfer and the provider is acceptable for the use case.

Risk: Email, SMS, scraping, and document or audio upload actions can affect third parties or external systems.

Mitigation: Require explicit user confirmation and review the generated command or payload before executing those actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/proactive-agent-hub)
- [Publisher profile](https://clawhub.ai/user/modestyrichards)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss models endpoint](https://api.heybossai.com/v1/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl examples, JSON request bodies, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; outputs may include links or generated content returned by external model providers through SkillBoss.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
