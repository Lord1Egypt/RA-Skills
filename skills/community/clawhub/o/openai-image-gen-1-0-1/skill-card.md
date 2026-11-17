## Description:

Batch-generate images via OpenAI Images API with a random prompt sampler and an index.html gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shi8103312](https://clawhub.ai/user/shi8103312)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate batches of images from random or custom prompts through the OpenAI Images API and review the outputs in a local thumbnail gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and an OpenAI API key over the network, and server security evidence notes that environment variables can redirect those requests to another endpoint.

Mitigation: Use only trusted API base URLs, keep OPENAI_BASE_URL and OPENAI_API_BASE unset unless intentionally configured, and avoid sensitive prompt content.

Risk: The generated HTML gallery displays prompt text and local image outputs.

Mitigation: Open galleries only from trusted runs and review prompt content before sharing generated output directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shi8103312/skills/openai-image-gen-1-0-1)
- [OpenAI API Endpoint](https://api.openai.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated runtime artifacts include PNG images, JSON prompt mappings, and an HTML gallery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenAI API key; supports count, model, prompt, size, output directory, quality, timeout, sleep, and dry-run options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
