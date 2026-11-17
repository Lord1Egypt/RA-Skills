## Description:

Helps agents prepare and submit PoYo Kling 3.0 4K video generation requests, including text-to-video, image-to-video, multi-shot payloads, polling, and webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Kling 3.0 4K video generation payloads, submit trusted asynchronous jobs, and guide polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep the key in server-side environment variables or a backend secret manager and avoid printing it in generated examples or command output.

Risk: Private prompts, source images, videos, or callback URLs may be sent to PoYo or a callback receiver during generation workflows.

Mitigation: Submit only content and callback endpoints the user has confirmed are appropriate for PoYo and the receiving service.

Risk: Live API submission can create external tasks when a prepared payload is run from a trusted shell.

Mitigation: Make live calls only after the user explicitly asks to submit a payload and POYO_API_KEY is available in the trusted environment.

## Reference(s):

- [PoYo Kling 3 API model page](https://poyo.ai/models/kling-3-api)
- [PoYo Kling 3.0 4K API docs](https://docs.poyo.ai/api-manual/video-series/kling-3-0-4k)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [Artifact API reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-3-0-4k)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit API requests only when explicitly requested and POYO_API_KEY is available in a trusted shell.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
