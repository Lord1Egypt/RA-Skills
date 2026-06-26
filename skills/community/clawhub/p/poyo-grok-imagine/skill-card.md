## Description: <br>
Use PoYo AI Grok Imagine Video for short text-to-video and image-to-video generation with motion-style controls through the PoYo generation endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Grok Imagine payloads, submit short video-generation jobs, and track the returned task identifier for polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, callback metadata, and generated-media workflow details are sent to PoYo. <br>
Mitigation: Install and use the skill only when PoYo is trusted for that data and avoid submitting sensitive prompts or image URLs unless approved. <br>
Risk: The skill requires a PoYo API key for authenticated requests. <br>
Mitigation: Set POYO_API_KEY through the environment or a secret manager and avoid passing credentials on the command line. <br>
Risk: Callback URLs may expose job metadata to external endpoints. <br>
Mitigation: Configure callback_url only for HTTPS endpoints that you control or explicitly trust. <br>


## Reference(s): <br>
- [PoYo Grok Imagine API Reference](references/api.md) <br>
- [PoYo Grok Imagine documentation](https://docs.poyo.ai/api-manual/video-series/grok-imagine) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Grok Imagine OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/grok-imagine.json) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-grok-imagine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chosen model id, payload summary, reference image usage, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
