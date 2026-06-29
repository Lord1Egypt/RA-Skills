## Description: <br>
Veo 3.1 Official video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `veo3.1-fast-official`, `veo3.1-lite-official`, `veo3.1-quality-official`, text-to-video, image-to-video, first/last-frame video, reference video, audio control, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Veo 3.1 Official video-generation payloads, submit trusted requests, and explain polling or webhook follow-up. It supports text-to-video, image-guided, first/last-frame, and reference-guided video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo may receive prompts, image or video URLs, callback URLs, and generation requests that can incur generated-content costs. <br>
Mitigation: Use the skill only when the user trusts PoYo for the supplied content and understands any cost implications. <br>
Risk: The POYO_API_KEY secret could be exposed through chat, logs, browser code, public repositories, or screenshots. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and avoid echoing or logging it. <br>
Risk: Live API calls submit generation jobs to an external service. <br>
Mitigation: Do not make live API calls unless the user explicitly asks and a safe server-side environment is available. <br>


## Reference(s): <br>
- [PoYo Veo 3.1 Official API Reference](references/api.md) <br>
- [PoYo Veo 3.1 Official Docs](https://docs.poyo.ai/api-manual/video-series/veo-3-1-official) <br>
- [PoYo Veo 3.1 Official Model Page](https://poyo.ai/models/veo-3-1-official) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl/bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the returned PoYo task_id when a request is explicitly submitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
