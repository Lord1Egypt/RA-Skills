## Description: <br>
Happy Horse video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `happy-horse`, text-to-video, image-to-video, reference-driven short video, video edit planning, task submission, polling, and webhook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare, submit, and follow up on PoYo Happy Horse video generation jobs for text-to-video, image-to-video, and reference-driven short video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY exposure could allow unauthorized use of the PoYo API. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and never include it in browser code, public repositories, logs, screenshots, or chat output. <br>
Risk: Prompt text, media URLs, and callback URLs may contain private or sensitive data. <br>
Mitigation: Review payloads before submission and avoid sending private prompts, media URLs, or callback URLs unless the user trusts PoYo to handle that data. <br>
Risk: Live submissions send requests to the external PoYo API. <br>
Mitigation: Make live API calls only when the user explicitly asks and a safe server-side environment is available. <br>


## Reference(s): <br>
- [PoYo Happy Horse API Reference](references/api.md) <br>
- [PoYo Happy Horse source docs](https://docs.poyo.ai/api-manual/video-series/happy-horse) <br>
- [PoYo Happy Horse model page](https://poyo.ai/models/happy-horse) <br>
- [PoYo Happy Horse example repository](https://github.com/PoyoAPI/happy-horse-api) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-happy-horse) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chosen model id, workflow type, request payload or parameter summary, task_id after submission, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
