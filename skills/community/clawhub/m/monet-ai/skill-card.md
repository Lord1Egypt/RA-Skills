## Description:

Monet AI provides agent-facing guidance for using the monet.vision API to generate video, images, and music across multiple AI generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekton](https://clawhub.ai/user/seekton)

### License/Terms of Use:


## Use Case:

Developers and AI agent builders use this skill to create authenticated monet.vision API requests for video, image, music, file upload, and task-status workflows. It is intended for content-generation pipelines that need concise model options, request formats, and polling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference media, audio, uploaded files, and task metadata are sent to a third-party Monet service.

Mitigation: Install and use the skill only when third-party processing by monet.vision is acceptable for the data involved.

Risk: Authenticated verbose curl output can expose request details or credentials in logs.

Mitigation: Remove the -v flag from authenticated examples unless logs are controlled and redacted; rotate MONET_API_KEY if verbose output may have been shared.

Risk: Repeated task creation can duplicate generation requests if retries do not use an idempotency key.

Mitigation: Use a unique idempotency_key, such as a UUID, for task creation requests.

## Reference(s):

- [Monet AI Skill Page](https://clawhub.ai/seekton/skills/monet-ai)
- [Monet Website](https://monet.vision)
- [Monet API Key Management](https://monet.vision/skills/keys)
- [Monet Async Task API](https://monet.vision/api/v1/tasks/async)
- [Monet Streaming Task API](https://monet.vision/api/v1/tasks/sync)
- [Monet File Upload API](https://monet.vision/api/v1/files)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONET_API_KEY; generated requests send prompts, metadata, and uploaded media to monet.vision.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
