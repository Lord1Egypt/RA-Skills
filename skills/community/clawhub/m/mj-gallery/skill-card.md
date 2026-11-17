## Description:

MXAI MJ image-generation and gallery skill that submits text-to-image requests, polls for completion, downloads images locally, archives them to a gallery folder, deploys the gallery, and returns accessible result links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate MJ images from prompts, preserve generated assets locally, and maintain a public web gallery of recent results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images and prompt-derived gallery metadata may be published in a public gallery.

Mitigation: Use only non-sensitive prompts and images unless publication consent and a local-only or cleanup workflow are added.

Risk: User-derived prompt text is inserted into gallery HTML without evidence of safe escaping.

Mitigation: Escape prompt and metadata fields before writing HTML and review generated pages before deployment.

Risk: The skill requires an MX_AI_API_KEY credential to submit image-generation requests.

Mitigation: Store the credential in the agent environment, avoid placing it in prompts or generated files, and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/mj-gallery)
- [ClawHub publisher profile](https://clawhub.ai/user/tianheihei002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown response with local image paths, public gallery links, and generated HTML gallery files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_AI_API_KEY; stores images under /workspace/mj_output and /workspace/mj_gallery; keeps the latest 20 gallery entries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
