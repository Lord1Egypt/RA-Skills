## Description: <br>
Wan 2.7 Image Pro generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `wan-2.7-image-pro`, text-to-image, image editing with one to four reference images, preset sizes, custom size objects, image count, seed, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to prepare PoYo Wan 2.7 Image Pro text-to-image and image-editing requests, submit trusted payloads, and plan polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API key exposure through browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and redact it from examples and logs. <br>
Risk: Unintended live PoYo submissions may process private prompts or source images and may create operational cost. <br>
Mitigation: Make live API calls only when the user explicitly asks, has a trusted server-side environment, and has reviewed the prepared payload. <br>
Risk: Private prompts, source image URLs, or callback URLs may be disclosed to PoYo or webhook receivers. <br>
Mitigation: Submit confidential inputs only when the user trusts PoYo and the callback endpoint, and avoid logging sensitive request or response details. <br>


## Reference(s): <br>
- [PoYo Wan 2.7 Image Pro API Reference](references/api.md) <br>
- [PoYo Wan 2.7 Image Pro Documentation](https://docs.poyo.ai/api-manual/image-series/wan-2-7-image-pro) <br>
- [PoYo Wan 2.7 Image Pro Model Page](https://poyo.ai/models/wan-2-7-image-pro) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-wan-2-7-image-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request type, payload summary, selected size, image count, reference image notes, task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
