## Description: <br>
Poyo Wan 2 5 helps agents prepare, submit, and follow up on PoYo Wan 2.5 text-to-video and image-to-video generation jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct Wan 2.5 text-to-video or image-to-video requests, submit prepared JSON payloads to PoYo, and plan polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A PoYo API key could be exposed through browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager and avoid echoing it in generated commands or responses. <br>
Risk: Prompts, image URLs, callback URLs, task IDs, or generated media may contain confidential information sent to PoYo or a callback receiver. <br>
Mitigation: Review payloads before submission and avoid sending confidential prompts, private image URLs, private callback URLs, or generated media unless the user trusts PoYo and the receiver. <br>
Risk: A prepared curl workflow can submit a live generation task if run in an environment with credentials. <br>
Mitigation: Make live API calls only after explicit user approval, with a reviewed payload, from a trusted shell environment. <br>


## Reference(s): <br>
- [PoYo Wan 2.5 Text-to-Video Docs](https://docs.poyo.ai/api-manual/video-series/wan2.5-text-to-video) <br>
- [PoYo Wan 2.5 Image-to-Video Docs](https://docs.poyo.ai/api-manual/video-series/wan2.5-image-to-video) <br>
- [PoYo Wan 2.5 Model Page](https://poyo.ai/models/wan-2-5) <br>
- [PoYo Wan 2.5 API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, curl examples, and optional shell command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live submission requires curl and POYO_API_KEY; otherwise the skill produces request guidance only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
