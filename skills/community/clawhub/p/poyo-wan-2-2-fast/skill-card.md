## Description: <br>
Helps agents prepare, submit, and follow up on PoYo Wan 2.2 Fast text-to-video and image-to-video generation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build PoYo Wan 2.2 Fast payloads, choose text-to-video or image-to-video models, submit asynchronous generation tasks, and explain polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed through browser code, logs, screenshots, chat output, or public repositories. <br>
Mitigation: Store POYO_API_KEY only in server-side environment variables or a backend secret manager, and avoid echoing or logging it. <br>
Risk: Prompts, image URLs, callback URLs, task IDs, and generated media URLs may reveal private or sensitive information to PoYo or a callback receiver. <br>
Mitigation: Submit only content the user is comfortable sharing with PoYo and the callback receiver; avoid confidential prompts and private media URLs. <br>
Risk: Live task submission sends network requests to PoYo and may create generation jobs. <br>
Mitigation: Make live API calls only after the user explicitly asks and provides a safe server-side environment. <br>


## Reference(s): <br>
- [PoYo Wan 2.2 Fast API Reference](references/api.md) <br>
- [PoYo Wan 2.2 Text-to-Video Fast Documentation](https://docs.poyo.ai/api-manual/video-series/wan2.2-text-to-video-fast) <br>
- [PoYo Wan 2.2 Image-to-Video Fast Documentation](https://docs.poyo.ai/api-manual/video-series/wan2.2-image-to-video-fast) <br>
- [PoYo Wan 2.2 Fast Model Page](https://poyo.ai/models/wan-2-2-fast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl or shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned PoYo task_id when a live request is submitted; live submission requires POYO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
