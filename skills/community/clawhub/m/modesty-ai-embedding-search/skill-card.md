## Description:

Build semantic search with embeddings through SkillBoss's OpenAI-compatible API gateway using a single SkillBoss API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure embedding-based semantic search and route requests through SkillBoss when they want an OpenAI-compatible interface and a single API key for multiple AI providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes task inputs and API requests through the external SkillBoss service.

Mitigation: Install only when the user accepts SkillBoss and downstream provider handling; avoid sensitive data unless those data-handling terms are understood.

Risk: The embedding-search label understates the broader third-party API gateway setup described by the artifact.

Mitigation: Review the remote setup guide before letting an agent follow it, and constrain use to the embedding-search or provider-routing behavior the user intends.

Risk: Remote setup instructions may change outside this reviewed release.

Mitigation: Prefer the pinned reviewed ClawHub release over unpinned clone or remote setup instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-ai-embedding-search)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss console](https://skillboss.co/console)
- [SkillBoss products](https://skillboss.co/products)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and routes requests through the external SkillBoss service.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
