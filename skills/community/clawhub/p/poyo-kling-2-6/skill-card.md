## Description:

Kling 2.6 video generation with native audio on PoYo, supporting text-to-video and image-to-video payload preparation, task submission, polling guidance, and webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and optionally submit PoYo Kling 2.6 video generation jobs with prompts, source images, audio settings, duration, aspect ratio, and callback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a PoYo API key to submit video-generation payloads.

Mitigation: Use a dedicated POYO_API_KEY with limited scope when available, store it server-side, and avoid exposing it in browser code, logs, screenshots, public repositories, or chat output.

Risk: Payloads can include prompts, media URLs, callback URLs, and generated media URLs that may be sensitive.

Mitigation: Review payload JSON before submission and avoid confidential prompts, private media URLs, private callback URLs, or generated media URLs unless the user trusts PoYo and the callback receiver.

Risk: Running the bundled curl helper on an untrusted machine can expose the API key to local process-inspection tools.

Mitigation: Run submissions only from a trusted shell after explicit user approval and use webhook or polling follow-up only for intended PoYo tasks.

## Reference(s):

- [PoYo Kling 2.6 API Reference](references/api.md)
- [PoYo Kling 2.6 Documentation](https://docs.poyo.ai/api-manual/video-series/kling-2-6)
- [PoYo Kling 2.6 Model Page](https://poyo.ai/models/kling-2-6)

## Skill Output:

**Output Type(s):** [guidance, markdown, json, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, request mode, payload summary, duration, aspect ratio, audio setting, source-image use, task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
