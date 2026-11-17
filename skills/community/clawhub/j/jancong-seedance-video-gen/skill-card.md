## Description:

Generates AI videos with Huoshan Engine Seedance 2.0 models through the Ark API, supporting text, image, video, and audio references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jancong](https://clawhub.ai/user/jancong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit Seedance 2.0 video generation jobs, poll task status, and retrieve generated video and cover files from the Ark platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Ark API key can be sent to any endpoint configured through ARK_API_URL.

Mitigation: Keep ARK_API_URL pinned to the official HTTPS Ark endpoint and use a limited-scope Ark API key.

Risk: Prompts and reference media URLs are sent to the external Ark service.

Mitigation: Avoid sensitive prompts, private media URLs, or confidential source material unless the environment and service use are approved.

Risk: The download script retrieves result URLs and writes files into the workspace.

Mitigation: Review or patch download behavior before using the skill in shared or important workspaces.

## Reference(s):

- [Seedance 2.0 API Reference](references/api_reference.md)
- [Seedance 2.0 Prompt Guide](references/prompt_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/jancong/skills/jancong-seedance-video-gen)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, API JSON responses, and downloaded video or cover files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated video tasks use configurable model, prompt, aspect ratio, duration, watermark, optional audio generation, and optional reference media URLs.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
