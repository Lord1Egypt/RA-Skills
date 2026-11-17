## Description:

Grok Imagine Image Quality generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use when the user explicitly requests PoYo or `grok-imagine-image-quality` for text-to-image, reference-image editing, aspect ratio, 1K or 2K output, output format, async polling, or webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Grok Imagine Image Quality text-to-image or reference-image editing requests, then explain async polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys can be exposed if placed in browser code, public files, logs, screenshots, chat output, or command-line telemetry.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager, use a narrowly scoped key on a trusted machine, avoid logging secrets, and rotate the key if exposure is possible.

Risk: Confidential prompts, private image URLs, result URLs, or callback URLs may be sent to PoYo or a callback receiver.

Mitigation: Submit only data the user is allowed to process and only when the user trusts PoYo and the callback receiver.

Risk: A live API call can submit a paid or persistent image-generation job.

Mitigation: Use the bundled submit helper only after explicit user approval and after reviewing the JSON payload.

## Reference(s):

- [PoYo Grok Imagine Image Quality API Reference](artifact/references/api.md)
- [PoYo Grok Imagine Image Quality model page](https://poyo.ai/models/grok-imagine-image-quality)
- [PoYo Grok Imagine Image Quality API docs](https://docs.poyo.ai/api-manual/image-series/grok-imagine-image-quality)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the exact model id, generation or editing mode, request payload, selected output controls, returned task_id, and next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
