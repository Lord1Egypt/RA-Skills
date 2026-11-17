## Description:

Generates asynchronous AI video requests from text prompts and public image URLs through OATDA's unified API across supported video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to submit video generation jobs to OATDA, choose an available provider/model, pass model-specific parameters, and track asynchronous task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and referenced public image URLs are sent to OATDA for video generation.

Mitigation: Use only content that is appropriate to share with OATDA and avoid including confidential or sensitive data in prompts or image URLs.

Risk: OATDA_API_KEY is required and could be exposed through shell history, logs, or command output.

Mitigation: Treat the API key as a secret, do not print full or partial key values, and prefer environment or credentials-file handling that keeps the key out of logs.

Risk: Copy-paste shell examples can become unsafe if user-provided prompt text is substituted directly into command strings.

Mitigation: Build request JSON with jq or another JSON encoder and validate or quote user-controlled values before execution.

## Reference(s):

- [OATDA](https://oatda.com)
- [OATDA Video Models API](https://oatda.com/api/v1/llm/models?type=video)
- [OATDA Generate Video API](https://oatda.com/api/v1/llm/generate-video?async=true)
- [ClawHub Skill Page](https://clawhub.ai/devcsde/skills/oatda-generate-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces asynchronous task IDs, polling guidance, and model/provider request parameters; generated videos are returned by the external OATDA service.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
