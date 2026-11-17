## Description:

Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate batches of OpenAI image outputs from random or user-supplied prompts and assemble the resulting PNG files, prompt mapping, and local HTML gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the OpenAI API key and prompts to a custom API endpoint if OPENAI_BASE_URL or OPENAI_API_BASE is set.

Mitigation: Run it in a clean environment where those variables are unset or intentionally trusted.

Risk: Prompts are sent to the image generation API and may contain confidential information.

Mitigation: Avoid confidential prompts and review prompt content before generation.

Risk: The generated local HTML gallery may include unescaped prompt content.

Mitigation: Review or patch the gallery generation before opening or hosting the generated index.html.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/openai-image-gen)

## Skill Output:

**Output Type(s):** [Files, Images, JSON, HTML]

**Output Format:** [PNG image files, JSON prompt mapping, and a local HTML gallery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs to a timestamped directory unless an explicit output directory is provided.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
