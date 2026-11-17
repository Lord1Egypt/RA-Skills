## Description:

Use PoYo AI Nano Banana for general image generation and image editing across supported aspect ratios through PoYo's image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to prepare, submit, and track PoYo Nano Banana image generation or image editing jobs. It helps choose the model variant, shape request payloads, submit authenticated API calls, and report returned task IDs for follow-up polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced image URLs, optional callback URLs, and the PoYo API key are sent to PoYo's service.

Mitigation: Use this skill only when PoYo is approved for the data involved, set POYO_API_KEY in the environment, and avoid sending secrets, private documents, internal URLs, or sensitive images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-nano-banana)
- [PoYo Nano Banana model page](https://poyo.ai/models/nano-banana-api)
- [PoYo Nano Banana API docs](https://docs.poyo.ai/api-manual/image-series/nano-banana)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [Artifact API reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a selected model id, request payload or parameter summary, reference-image status, returned task_id, and next-step polling or webhook guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
