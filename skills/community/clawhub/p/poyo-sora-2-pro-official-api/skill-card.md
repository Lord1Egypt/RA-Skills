## Description: <br>
Sora 2 Pro Official video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `sora-2-pro-official`, text-to-video, optional single-image guidance, aspect ratio control, 4 to 20 second clips, 720p, 1024p, or 1080p output, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare and submit PoYo Sora 2 Pro Official text-to-video or single-image guided video jobs, then track completion through polling or webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live submission can create external asynchronous PoYo generation jobs and may incur provider usage. <br>
Mitigation: Run the submit script only when the user explicitly requests live execution and a trusted server-side environment is configured. <br>
Risk: Prompts, source image URLs, callback URLs, and API credentials can be exposed to external services or logs if handled carelessly. <br>
Mitigation: Keep POYO_API_KEY in server-side secrets, avoid logging sensitive payload fields, and submit confidential images or callback URLs only when the user trusts PoYo and the callback receiver. <br>


## Reference(s): <br>
- [PoYo Sora 2 Pro Official API documentation](https://docs.poyo.ai/api-manual/video-series/sora-2-pro-official) <br>
- [PoYo Sora 2 Pro Official model page](https://poyo.ai/models/sora-2-pro-official) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-sora-2-pro-official-api) <br>
- [Bundled API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and optional curl or shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request type, payload fields, selected duration, aspect ratio, resolution, task_id, and next-step polling or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
