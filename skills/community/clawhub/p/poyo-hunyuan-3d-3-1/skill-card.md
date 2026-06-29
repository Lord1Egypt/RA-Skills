## Description: <br>
Hunyuan 3D v3.1 asset generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `hunyuan-3d/v3.1/pro/text-to-3d`, `hunyuan-3d/v3.1/pro/image-to-3d`, `hunyuan-3d/v3.1/rapid/text-to-3d`, `hunyuan-3d/v3.1/rapid/image-to-3d`, text-to-3D, image-to-3D, PBR, geometry, face count, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical artists use this skill to plan, prepare, and submit PoYo Hunyuan 3D v3.1 text-to-3D or image-to-3D asset generation jobs. It helps select Pro or Rapid model IDs, shape request payloads, handle API-key use, and identify the next polling or webhook step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound API calls using POYO_API_KEY, which is a secret credential. <br>
Mitigation: Use a server-side environment or secret manager, use least-privileged keys when available, and avoid exposing keys in chat, logs, browser code, screenshots, or public repositories. <br>
Risk: Submitting confidential prompts, object images, private asset URLs, or callback URLs sends that material to PoYo and any configured callback receiver. <br>
Mitigation: Submit only material the user is allowed to share with PoYo and the callback receiver, and avoid live API calls unless the user explicitly requests them from a trusted server-side shell. <br>


## Reference(s): <br>
- [PoYo Hunyuan 3D v3.1 API Reference](references/api.md) <br>
- [PoYo Hunyuan 3D v3.1 Documentation](https://docs.poyo.ai/api-manual/3d-series/hunyuan-3d-3-1) <br>
- [PoYo Hunyuan 3D v3.1 Model Page](https://poyo.ai/models/hunyuan-3d-3-1) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-hunyuan-3d-3-1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with JSON payloads and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model ID, text-to-3D or image-to-3D workflow summary, request payload, material and geometry settings, task ID, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
