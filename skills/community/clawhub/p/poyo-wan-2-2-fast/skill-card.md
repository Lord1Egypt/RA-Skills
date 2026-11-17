## Description:

Helps agents prepare and submit PoYo Wan 2.2 Fast text-to-video and image-to-video jobs, including payload fields, async task submission, polling, and webhook guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Wan 2.2 Fast video-generation requests, choose the correct text-to-video or image-to-video model, submit prepared payloads, and plan polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys and bearer tokens may be exposed if commands are run on shared systems or logged.

Mitigation: Use a scoped PoYo API key where possible, keep it in a trusted server-side environment, avoid logging commands or headers, and consider hardening script execution before shared-system use.

Risk: Prompts, private media URLs, callback URLs, task IDs, or generated video URLs may contain confidential information.

Mitigation: Submit confidential prompts or private media only when the user trusts PoYo and the callback receiver; avoid logging private request and response data.

## Reference(s):

- [PoYo Wan 2.2 Fast model page](https://poyo.ai/models/wan-2-2-fast)
- [PoYo Wan 2.2 Text-to-Video Fast API docs](https://docs.poyo.ai/api-manual/video-series/wan2.2-text-to-video-fast)
- [PoYo Wan 2.2 Image-to-Video Fast API docs](https://docs.poyo.ai/api-manual/video-series/wan2.2-image-to-video-fast)
- [Local PoYo Wan 2.2 Fast API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and optional bash or curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, request type, resolution, aspect ratio, seed, source image count, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
