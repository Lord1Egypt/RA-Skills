## Description:

Helps agents prepare, submit, and follow up on PoYo Seedream 4 image generation and editing requests, including payloads, curl commands, polling, and callback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when a user has chosen PoYo Seedream 4 and needs server-side request payloads, curl examples, async task submission, status polling, webhook setup, or response parsing for text-to-image and image-editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys or authorization headers could be exposed if examples are copied into browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and redact authorization headers from logs and responses.

Risk: Payloads may contain private prompts, source image URLs, callback URLs, generated outputs, or task IDs that are sent to PoYo or exposed through logging.

Mitigation: Review payload JSON before submission, and send or log private data only when project policy permits PoYo processing.

Risk: The helper can submit externally processed image-generation jobs when used with a real API key.

Mitigation: Make live API calls only after explicit user approval from a trusted server-side shell.

## Reference(s):

- [PoYo Seedream 4 API reference](references/api.md)
- [PoYo Seedream 4 model page](https://poyo.ai/models/seedream-4)
- [PoYo Seedream 4 API docs](https://docs.poyo.ai/api-manual/image-series/seedream-4)
- [PoYo Seedream 4 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/seedream-4.json)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedream-4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo request payloads, polling steps, webhook notes, and task IDs after approved submission.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
