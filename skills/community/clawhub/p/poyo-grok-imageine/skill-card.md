## Description: <br>
Helps agents prepare, submit, and explain PoYo Grok Imagine text-to-video and image-to-video generation jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with short Grok Imagine video generation jobs on PoYo, including prompt setup, optional reference images, duration, aspect ratio, mode selection, and status follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A PoYo API key can be exposed if copied into prompts, logs, or shared shell history. <br>
Mitigation: Keep POYO_API_KEY private, prefer environment variables or secret storage, and avoid printing credentials in generated examples. <br>
Risk: Prompts and optional image URLs are sent to PoYo for processing. <br>
Mitigation: Avoid sensitive prompts or private image URLs unless that processing is acceptable for the use case. <br>
Risk: Webhook callbacks can send task results to the wrong destination if an untrusted callback URL is used. <br>
Mitigation: Use only trusted HTTPS callback URLs controlled by the user, or omit callbacks and poll task status instead. <br>


## Reference(s): <br>
- [PoYo Grok Imagine API Reference](references/api.md) <br>
- [PoYo Grok Imagine Documentation](https://docs.poyo.ai/api-manual/video-series/grok-imagine) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Grok Imagine OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/grok-imagine.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payload examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the model id, payload summary, reference image use, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
