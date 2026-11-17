## Description:

Poyo Sora 2 helps agents prepare, submit, and track PoYo AI Sora 2 text-to-video and image-to-video generation jobs through the PoYo generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to build PoYo-compatible Sora 2 request payloads, submit text-to-video or image-to-video jobs, and report task IDs for follow-up polling or webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing a PoYo API key as a command-line argument can expose the secret through shell history or process listings.

Mitigation: Prefer POYO_API_KEY from the environment or a secret manager, and avoid supplying the key as a positional argument.

Risk: Prompts, callback URLs, and image URLs are sent to PoYo when generation jobs are submitted.

Mitigation: Submit only payloads the user is comfortable sharing with PoYo, especially when handling sensitive images or callback endpoints.

Risk: Successful video-generation requests may consume account quota or paid credits.

Mitigation: Confirm the intended model, duration, and generation mode before submitting requests that use the user's PoYo account.

## Reference(s):

- [PoYo Sora 2 API Reference](references/api.md)
- [PoYo Sora 2 Model Page](https://poyo.ai/models/sora-2)
- [PoYo Sora 2 API Docs](https://docs.poyo.ai/api-manual/video-series/sora-2)
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status)
- [Poyo Sora 2 ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-sora-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model, generation mode, request payload, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
