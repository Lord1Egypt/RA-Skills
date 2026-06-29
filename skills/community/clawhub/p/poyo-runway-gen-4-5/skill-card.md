## Description: <br>
Runway Gen-4.5 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `runway-gen-4.5`, text-to-video, optional single-image guidance, 5 or 10 second clips, aspect ratio control, seeded output, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and optionally submit PoYo Runway Gen-4.5 text-to-video or single-image guided video generation tasks. It helps assemble request payloads, choose duration and aspect ratio, handle polling or webhooks, and report task identifiers after submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API credentials could be exposed if included in browser code, public files, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing credentials in examples or outputs. <br>
Risk: Live submissions may send private prompts, source image URLs, or callback URLs to a third-party API. <br>
Mitigation: Make live API calls only after an explicit user request from a trusted server-side shell, and avoid submitting confidential inputs unless the user accepts the provider and callback receiver. <br>


## Reference(s): <br>
- [PoYo Runway Gen-4.5 API documentation](https://docs.poyo.ai/api-manual/video-series/runway-gen-4-5) <br>
- [PoYo Runway Gen-4.5 model page](https://poyo.ai/models/runway-gen-4-5) <br>
- [ClawHub skill listing](https://clawhub.ai/coolhackboy/poyo-runway-gen-4-5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and curl or bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id when the user explicitly requests a live API submission from a trusted shell.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
