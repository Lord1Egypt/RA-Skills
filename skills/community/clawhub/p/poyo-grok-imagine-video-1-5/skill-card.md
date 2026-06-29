## Description: <br>
Helps agents prepare PoYo Grok Imagine Video 1.5 image-to-video requests, submit trusted JSON payloads, and guide polling or webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare single-source-image Grok Imagine Video 1.5 requests on PoYo, submit trusted JSON payloads with curl, and explain task status polling or webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and redact it from generated examples and logs. <br>
Risk: Source images, prompts, callback URLs, or generated video URLs may contain private information. <br>
Mitigation: Submit only media and prompts the user is comfortable sending to PoYo and avoid logging private image URLs, prompts, callback URLs, or final video URLs. <br>
Risk: Live API submission can create external tasks and consume account resources. <br>
Mitigation: Make live calls only when the user explicitly requests submission from a trusted shell and provides a prepared payload. <br>


## Reference(s): <br>
- [PoYo Grok Imagine Video 1.5 API documentation](https://docs.poyo.ai/api-manual/video-series/grok-imagine-video-1-5) <br>
- [PoYo Grok Imagine Video 1.5 model page](https://poyo.ai/models/grok-imagine-video-1-5) <br>
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-grok-imagine-video-1-5) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/coolhackboy) <br>
- [Bundled API reference](artifact/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id when the user explicitly requests a live submission from a trusted shell.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
