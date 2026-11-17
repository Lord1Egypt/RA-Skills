## Description:

Upscale hosted videos on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `poyo-ai/video-upscaler`, public video URLs, scale control, async status polling, callbacks, and server-side integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare PoYo video-upscaling payloads, submit async tasks for publicly hosted video files, and plan status polling or callback handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY exposure could allow unauthorized use of the PoYo account.

Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager, and do not place it in browser code, logs, public repositories, screenshots, or chat output.

Risk: Submitting private video URLs or callback URLs to the hosted PoYo service may disclose sensitive workflow data.

Mitigation: Review each JSON payload before submission and avoid sending private video or callback URLs unless that is acceptable for the workflow.

Risk: Unintended live API submissions can create tasks against the user's PoYo account.

Mitigation: Make live API calls only after the user confirms the payload and provides a safe server-side environment.

## Reference(s):

- [PoYo Video Upscaler API Reference](references/api.md)
- [PoYo Video Upscaler Model Page](https://poyo.ai/models/video-upscaler)
- [Poyo Video Upscaler on ClawHub](https://clawhub.ai/coolhackboy/skills/poyo-video-upscaler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo model id, source video URL notes, selected scale, final request payload, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
