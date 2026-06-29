## Description: <br>
Kling O3 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-o3/standard`, `kling-o3/pro`, text-to-video, image-to-video, reference-to-video, multi_shots, multi_prompt, sound, aspect ratio control, element references, polling, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit PoYo Kling O3 video generation jobs, including text-to-video, image-to-video, reference-to-video, and multi-shot workflows. It also guides polling, webhook follow-up, and safe handling of API keys and private media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a PoYo API key and can submit requests to an external video generation service. <br>
Mitigation: Keep `POYO_API_KEY` in a server-side environment or secret manager, avoid exposing it in client code, logs, screenshots, or chat output, and make live API calls only when explicitly requested. <br>
Risk: Prompts, source images, reference images, generated videos, and callback URLs may be sensitive. <br>
Mitigation: Submit sensitive media, prompts, or callback URLs only when the user trusts PoYo and the callback receiver. <br>


## Reference(s): <br>
- [PoYo Kling O3 API Reference](references/api.md) <br>
- [PoYo Kling O3 Documentation](https://docs.poyo.ai/api-manual/video-series/kling-o3) <br>
- [PoYo Kling O3 Model Page](https://poyo.ai/models/kling-o3) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model selection, request payloads, curl commands, task IDs, polling guidance, and webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
