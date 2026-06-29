## Description: <br>
Kling 1.6 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-1.6/standard`, `kling-1.6/pro`, text-to-video, image-to-video, start and end frame guidance, elements with reference images, duration, aspect ratio, negative prompt, cfg scale, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare, submit, and follow up on PoYo Kling 1.6 video-generation jobs for text-to-video, image-to-video, first/last-frame, and element-reference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits prompts, image URLs, callback URLs, and API credentials to PoYo endpoints. <br>
Mitigation: Use it only when PoYo is the intended provider, keep POYO_API_KEY in a server-side environment, and review payloads before submission. <br>
Risk: Private prompts, source images, reference images, or callback URLs may expose sensitive information to PoYo or the callback receiver. <br>
Mitigation: Avoid sending private content unless the user trusts PoYo and the callback receiver for that data. <br>
Risk: Live API submission can create asynchronous video-generation tasks and external network activity. <br>
Mitigation: Make live calls only from a trusted shell after explicit user approval, then save the returned task_id for controlled polling or webhook follow-up. <br>


## Reference(s): <br>
- [PoYo Kling 1.6 API Reference](references/api.md) <br>
- [PoYo Kling 1.6 Documentation](https://docs.poyo.ai/api-manual/video-series/kling-1-6) <br>
- [PoYo Kling 1.6 Model Page](https://poyo.ai/models/kling-1-6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model selection, request payload summaries, submitted task IDs, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
