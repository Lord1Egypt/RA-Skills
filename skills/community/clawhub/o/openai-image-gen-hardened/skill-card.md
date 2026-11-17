## Description:

Batch-generate images via OpenAI Images API with a random prompt sampler and local index.html gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate batches of images from OpenAI image models, customize model parameters, and review the local image outputs in an HTML gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated gallery can render user-controlled prompt text as active HTML.

Mitigation: HTML-escape prompt and path values before writing index.html, especially when using shared or untrusted prompt text.

Risk: Prompts are sent to OpenAI's Images API and generated outputs are stored locally.

Mitigation: Use only prompts and output locations approved for the deployment context, and keep OPENAI_API_KEY in the environment rather than logs, arguments, or generated artifacts.

## Reference(s):

- [OpenAI Images API Reference](https://platform.openai.com/docs/api-reference/images)
- [ClawHub skill release](https://clawhub.ai/snazar-faberlens/skills/openai-image-gen-hardened)
- [Faberlens safety evaluation](https://faberlens.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces image files, prompts.json, and a local index.html gallery; requires python3 and OPENAI_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
