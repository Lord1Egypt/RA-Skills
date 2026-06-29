## Description: <br>
Sora 2 Official video generation on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit for text-to-video, optional single-image guided video, supported durations, aspect ratios, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit PoYo Sora 2 Official text-to-video or image-guided video jobs, then explain task polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY could be exposed if placed in browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid echoing it in commands or responses. <br>
Risk: Submitted prompts, image URLs, and callback URLs may contain confidential or private information. <br>
Mitigation: Review payload JSON before submission and only send confidential prompts, private image URLs, or sensitive callback URLs when the user trusts PoYo and the callback receiver. <br>
Risk: The helper can submit a live network request to PoYo and create an asynchronous video-generation task. <br>
Mitigation: Make live API calls only after explicit user approval in a trusted server-side shell, then record the returned task_id for polling or webhook follow-up. <br>


## Reference(s): <br>
- [PoYo Sora 2 Official API docs](https://docs.poyo.ai/api-manual/video-series/sora-2-official) <br>
- [PoYo Sora 2 Official model page](https://poyo.ai/models/sora-2-official) <br>
- [Local API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON payload examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a selected model id, text-to-video or image-guided mode, payload summary, duration, aspect ratio, reference image status, task_id after submission, and next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
