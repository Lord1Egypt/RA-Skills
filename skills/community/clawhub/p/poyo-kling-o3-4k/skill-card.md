## Description: <br>
Kling O3 4K video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-o3/4K`, text-to-video, image-to-video, reference-to-video, multi_shots, multi_prompt, sound, aspect ratio control, element references, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Kling O3 4K video generation payloads, submit trusted async jobs, and explain polling or webhook follow-up for text-to-video, image-to-video, reference-to-video, and multi-shot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a trusted server-side environment or backend secret manager and avoid echoing it in generated commands or responses. <br>
Risk: Submitting a payload sends prompts, media URLs, and optional callback URLs to PoYo and may trigger external processing. <br>
Mitigation: Review payloads before running the helper script and submit only when the user explicitly asks from a trusted shell. <br>
Risk: Private prompts, source media, generated videos, or callback URLs may be sensitive. <br>
Mitigation: Avoid sending sensitive inputs unless the user trusts PoYo and the callback receiver. <br>


## Reference(s): <br>
- [PoYo Kling O3 4K API manual](https://docs.poyo.ai/api-manual/video-series/kling-o3-4k) <br>
- [PoYo Kling O3 4K model page](https://poyo.ai/models/kling-o3-4k) <br>
- [Artifact API reference](artifact/references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o3-4k) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and bash/curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model id, request mode, payload summary or final JSON, duration, aspect ratio, sound setting, media/reference inputs, task_id after submission, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
