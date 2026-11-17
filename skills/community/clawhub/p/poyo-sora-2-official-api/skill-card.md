## Description:

Helps agents prepare, submit, and follow up on Sora 2 Official video-generation jobs on PoYo using text-to-video or single-image guided video payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create PoYo Sora 2 Official request payloads, submit reviewed video-generation tasks, and understand polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid echoing credentials.

Risk: Prompts, private image URLs, or callback URLs may disclose sensitive information to PoYo or a receiving webhook.

Mitigation: Submit only reviewed payloads and avoid confidential prompts, private image URLs, or sensitive callback URLs unless the user trusts PoYo and the callback receiver.

Risk: Live submissions can spend quota or send unintended video-generation requests.

Mitigation: Make live API calls only when the user explicitly asks and a safe server-side POYO_API_KEY environment is available.

## Reference(s):

- [PoYo Sora 2 Official API Reference](references/api.md)
- [PoYo Sora 2 Official model page](https://poyo.ai/models/sora-2-official)
- [PoYo Sora 2 Official API docs](https://docs.poyo.ai/api-manual/video-series/sora-2-official)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo model id, request type, duration, aspect ratio, reference-image status, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
