## Description:

Seedream 5.0 Lite image generation and editing on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit; use for seedream-5.0-lite, seedream-5.0-lite-edit, 2K/3K output, multi-reference editing, and aspect-ratio control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and submit PoYo Seedream 5.0 Lite text-to-image and image-editing requests, including model choice, payload fields, high-resolution or aspect-ratio sizing, and follow-up polling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can accept the PoYo API key as a command-line argument, which may expose the key in shell history, process listings, or logs.

Mitigation: Set POYO_API_KEY through a protected environment or secret manager and avoid passing the key as a command-line argument.

Risk: Prompts and reference image URLs are sent to PoYo's API for generation or editing.

Mitigation: Avoid submitting private prompts or sensitive reference image URLs unless sharing them with PoYo is acceptable for the use case.

## Reference(s):

- [PoYo Seedream 5.0 Lite model page](https://poyo.ai/models/seedream-5-0-lite-api)
- [PoYo Seedream 5.0 Lite API docs](https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite)
- [PoYo Seedream 5.0 Lite OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite.json)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedream-5-0-lite)
- [Local API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When a request is submitted, the skill reports the chosen model id, payload or parameter summary, reference image involvement, returned task_id, and next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
