## Description:

Kling Avatar 2.0 video generation on PoYo via the PoYo submit API, including model selection, payload preparation, polling guidance, webhook guidance, and optional trusted-shell submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Kling Avatar 2.0 avatar-video requests from one reference image and one driving audio URL, then submit or explain follow-up polling and webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY can be exposed if copied into browser code, logs, repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing it in generated examples or command output.

Risk: Avatar images, driving audio, prompts, and callback URLs may contain private or sensitive data sent to PoYo or a callback receiver.

Mitigation: Review the payload before submission and use private likenesses, confidential audio, private prompts, or private callback URLs only when the user trusts PoYo and the callback receiver.

Risk: The helper script can make a live PoYo API request when run with a payload and valid API key.

Mitigation: Run the script only after explicit user intent, from a trusted shell, with a reviewed JSON payload.

## Reference(s):

- [PoYo Kling Avatar 2.0 API Reference](references/api.md)
- [PoYo Kling Avatar 2.0 model page](https://poyo.ai/models/kling-avatar-2-0)
- [PoYo Kling Avatar 2.0 API docs](https://docs.poyo.ai/api-manual/video-series/kling-avatar-2-0)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-avatar-2-0)
- [ClawHub publisher profile](https://clawhub.ai/user/coolhackboy)

## Skill Output:

**Output Type(s):** [text, markdown, JSON payloads, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, payload summary, media roles, optional prompt guidance, returned task_id, and next-step polling or webhook guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
