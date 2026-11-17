## Description:

Jimeng Video helps agents generate audio-enabled AI videos through the Volcengine/Dreamina API, supporting text-to-video, image-to-video, multiple models, batch generation, and task status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content operators, advertisers, and developers use this skill to ask an agent for short-form AI video generation with optional generated audio, then create, batch, monitor, and retrieve Volcengine/Dreamina generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded images, credentials, and generated task data may be sent to the Volcengine/Dreamina cloud service.

Mitigation: Use scoped API credentials, keep secrets private, and avoid sending sensitive prompts or images unless the external service use is acceptable.

Risk: Broad video-generation requests could activate third-party API usage unexpectedly.

Mitigation: Confirm user intent before invoking Volcengine/Dreamina generation tasks and review generated outputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/jimeng-video-v1)
- [Volcengine content generation tasks API](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or retrieve video task outputs through the Volcengine/Dreamina service when credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
