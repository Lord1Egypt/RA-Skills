## Description: <br>
Kling O3 image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-o3-image`, `kling-o3-image-edit`, prompt-only image generation, reference-image editing, element descriptors, 1K, 2K, 4K output, aspect ratio control, output format, image count, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Kling O3 prompt-only image generation or reference-image editing requests, submit prepared JSON payloads when explicitly asked, and guide polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Store `POYO_API_KEY` only in server-side environment variables or a backend secret manager, and avoid echoing secrets in generated commands or responses. <br>
Risk: Private prompts, source image URLs, or callback URLs may be sent to PoYo or a webhook receiver during task submission. <br>
Mitigation: Submit only user-approved payloads from trusted environments, and avoid confidential prompts, private image URLs, or callback URLs unless the user trusts PoYo and the webhook receiver. <br>
Risk: A live API call can start an external image-generation task and consume account resources. <br>
Mitigation: Do not make live PoYo API calls unless the user explicitly requests submission and has provided a safe server-side environment. <br>


## Reference(s): <br>
- [PoYo Kling O3 API documentation](https://docs.poyo.ai/api-manual/image-series/kling-o3) <br>
- [PoYo Kling O3 model page](https://poyo.ai/models/kling-o3-image) <br>
- [Artifact API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o3-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model choice, request type, payload summary, selected resolution, aspect ratio, output format, image count, task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
