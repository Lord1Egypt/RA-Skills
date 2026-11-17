## Description:

Seedream 5.0 Pro image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedream-5.0-pro`, `seedream-5.0-pro-edit`, text-to-image, reference-image editing, 1K or 2K output, aspect-ratio control, and multi-image output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and optionally submit reviewed Seedream 5.0 Pro image generation or image-editing payloads to PoYo, then report the returned task ID and next status-check step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, callback URLs, generated image URLs, and API keys are sent to or handled around PoYo.

Mitigation: Use the skill only in a trusted environment, avoid sensitive payload contents unless appropriate, keep POYO_API_KEY in a server-side secret store, and do not place sensitive URLs or keys in logs or chat output.

Risk: Local process command lines or monitoring may expose the API key or request details.

Mitigation: Pass the API key through the POYO_API_KEY environment variable, review payload files before submission, and rotate POYO_API_KEY if local process command lines may have been logged or monitored.

Risk: Live image-generation submissions can send private reference images or callback endpoints outside the local environment.

Mitigation: Make live API calls only after explicit user approval for a reviewed payload and only when the user trusts PoYo and any callback receiver.

## Reference(s):

- [PoYo Seedream 5.0 Pro API Reference](references/api.md)
- [PoYo Seedream 5.0 Pro model page](https://poyo.ai/models/seedream-5-0-pro)
- [PoYo Seedream 5.0 Pro API docs](https://docs.poyo.ai/api-manual/image-series/seedream-5-0-pro)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedream-5-pro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payload summaries and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model, mode, payload summary, reference-image count, output settings, returned task_id, and next status-check step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
