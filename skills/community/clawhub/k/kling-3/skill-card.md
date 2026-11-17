## Description:

Kling 3.0 video generation on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `kling-3.0/standard`, `kling-3.0/pro`, text-to-video, image-to-video, multi-shot prompts, element references, sound-enabled output, polling, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to prepare or submit PoYo Kling 3.0 text-to-video, image-to-video, multi-shot, and element-referenced generation requests, then track returned task IDs through polling or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, callback URLs, and generation metadata are sent to PoYo.

Mitigation: Use the skill only when the user trusts PoYo for the submitted content, and avoid confidential prompts, source image URLs, or private callback endpoints.

Risk: The PoYo API key may be exposed through process arguments when using the submit script.

Mitigation: Keep POYO_API_KEY in a protected server-side environment and prefer a safer client or revised submission path that avoids exposing bearer tokens in process arguments.

## Reference(s):

- [PoYo Kling 3.0 API Reference](references/api.md)
- [PoYo Kling 3 API model page](https://poyo.ai/models/kling-3-api)
- [PoYo Kling 3.0 API documentation](https://docs.poyo.ai/api-manual/video-series/kling-3-0)
- [ClawHub Kling 3 skill page](https://clawhub.ai/coolhackboy/skills/kling-3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payloads and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, generation mode, payload summary or full payload, reference image or element details, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
