## Description: <br>
Kling O1 image editing on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit; use for kling-o1-image-edit, reference-image editing, element descriptors, character or object control, 1K, 2K output, aspect ratio, output format, image count, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Kling O1 image-editing requests, submit user-approved asynchronous jobs, and explain polling or webhook follow-up for generated image results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY exposure could allow unauthorized use of the PoYo API. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and never place it in browser code, repositories, logs, screenshots, or chat output. <br>
Risk: Private prompts, source image URLs, callback URLs, or generated image URLs may contain confidential information. <br>
Mitigation: Review payloads before submission and send confidential inputs only when the user trusts PoYo and the callback receiver. <br>
Risk: The helper can submit live image-editing jobs to an external API. <br>
Mitigation: Make live API calls only after explicit user approval from a trusted shell with a prepared payload. <br>


## Reference(s): <br>
- [PoYo Kling O1 Image API Reference](artifact/references/api.md) <br>
- [PoYo Kling O1 API Documentation](https://docs.poyo.ai/api-manual/image-series/kling-o1) <br>
- [PoYo Kling O1 Image Model Page](https://poyo.ai/models/kling-o1-image) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o1-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash or curl examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a selected model id, request payload summary, task_id after submission, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
