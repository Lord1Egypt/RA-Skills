## Description:

Helps agents prepare PoYo Flux Kontext image generation and single-image editing requests, including model selection, payload fields, polling, webhook guidance, and optional task submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create PoYo Flux Kontext text-to-image and image-editing payloads, choose supported Pro or Max model IDs, and guide async task submission, polling, or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if placed in browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Store POYO_API_KEY only in a server-side secret store or trusted shell environment and avoid echoing it in generated examples or responses.

Risk: Prompts, source image URLs, and callback URLs are submitted to PoYo when live API calls are made.

Mitigation: Submit only content and callback endpoints the user is comfortable sending to PoYo, and make live calls only after explicit user request in a trusted environment.

## Reference(s):

- [PoYo Flux Kontext model page](https://poyo.ai/models/flux-kontext)
- [PoYo Flux Kontext API documentation](https://docs.poyo.ai/api-manual/image-series/flux-kontext)
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key)
- [API reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo model IDs, task payloads, polling instructions, webhook guidance, and task IDs when a live submit is requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
