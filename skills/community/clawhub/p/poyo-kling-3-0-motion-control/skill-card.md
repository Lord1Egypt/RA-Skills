## Description: <br>
Kling 3.0 motion control video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-3.0-motion-control`, one reference image plus one reference video, character orientation control, optional prompts, 720p or 1080p output, optional element references, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and optionally submit PoYo Kling 3.0 motion-control video jobs from one reference image and one reference video, then guide polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if included in browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep `POYO_API_KEY` server-side in environment variables or a backend secret manager and avoid echoing it in generated examples or results. <br>
Risk: Private images, videos, prompts, or callback URLs could be sent to PoYo or a receiving endpoint unintentionally. <br>
Mitigation: Review payloads before submission and submit private media, prompts, or callback URLs only when the user trusts PoYo and the callback receiver. <br>
Risk: Live API submission can start an asynchronous video-generation task and may incur external processing. <br>
Mitigation: Make live API calls only after the user explicitly asks and provides a trusted server-side environment. <br>


## Reference(s): <br>
- [PoYo Kling 3.0 Motion Control API Reference](references/api.md) <br>
- [PoYo Kling 3.0 Motion Control documentation](https://docs.poyo.ai/api-manual/video-series/kling-3-0-motion-control) <br>
- [PoYo Kling 3.0 Motion Control model page](https://poyo.ai/models/kling-3-0-motion-control) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-kling-3-0-motion-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON payloads and curl or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model id, payload summary, media roles, character orientation, resolution, optional element references, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
