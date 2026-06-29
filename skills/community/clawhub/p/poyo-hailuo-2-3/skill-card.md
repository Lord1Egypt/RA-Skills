## Description: <br>
Helps agents prepare, submit, and follow up on PoYo Hailuo 2.3 video generation requests, including text-to-video and first-frame guided workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Hailuo 2.3 request payloads, submit trusted PoYo API jobs, and explain polling or webhook follow-up. It is suited for short video generation workflows that need duration, resolution, optional first-frame image guidance, and prompt optimization choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, private prompts, source image URLs, or callback URLs could be exposed if included in logs, browser code, screenshots, repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a trusted server-side secret store and redact keys, private prompts, image URLs, and callback URLs from shared output. <br>
Risk: Submitting live video generation jobs can send user content to PoYo and may incur cost or disclose sensitive creative material. <br>
Mitigation: Only make live API calls after explicit user confirmation in a trusted environment, and avoid confidential prompts or source images unless the user accepts the PoYo workflow. <br>
Risk: Generated request parameters or model options may become stale as PoYo updates Hailuo 2.3 support. <br>
Mitigation: Check the current PoYo documentation before relying on duration, resolution, first-frame, or prompt optimization options for production use. <br>


## Reference(s): <br>
- [PoYo Hailuo 2.3 API documentation](https://docs.poyo.ai/api-manual/video-series/hailuo-2-3) <br>
- [PoYo Hailuo 2.3 model page](https://poyo.ai/models/hailuo-2-3) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-hailuo-2-3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and curl or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request mode, duration, resolution, prompt optimizer setting, task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
