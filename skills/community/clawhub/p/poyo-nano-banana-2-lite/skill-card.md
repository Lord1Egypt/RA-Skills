## Description:

Poyo Nano Banana 2 Lite helps agents prepare and submit PoYo image generation and lightweight image editing jobs for nano-banana-2-lite and nano-banana-2-lite-edit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Nano Banana 2 Lite text-to-image and image-editing requests, prepare JSON payloads, and submit reviewed asynchronous image jobs from a trusted shell.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API key exposure could allow unauthorized image-generation requests.

Mitigation: Keep POYO_API_KEY in a trusted server-side environment or secret manager, and do not place it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Prompts, source image URLs, callback URLs, and generated output URLs may contain private or sensitive information.

Mitigation: Avoid sending or logging private prompts and image URLs unless that is acceptable for the workflow and the user has approved the data handling.

Risk: Submitting an unreviewed payload can send unintended model, prompt, image, or callback data to PoYo.

Mitigation: Run the submit script only with payloads that have been reviewed in a trusted shell environment.

## Reference(s):

- [PoYo Nano Banana 2 Lite model page](https://poyo.ai/models/nano-banana-2-lite)
- [PoYo Nano Banana 2 Lite API docs](https://docs.poyo.ai/api-manual/image-series/nano-banana-2-lite)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id when a reviewed API submission is actually made.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
