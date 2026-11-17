## Description:

Enhances garment texture and reconstructs fabric detail in product images using a high-resolution reference photo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce image editors and apparel teams use this skill to guide restoration of fabric texture in an existing product or on-model photo while preserving the source image's garment, person, framing, and background.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious because it flags image transfers to external image services without clear privacy disclosure; several components were only partially analyzed.

Mitigation: Before running, check the selected provider's image handling terms and upload only images you are permitted to share; use a provider whose data handling is acceptable for the material.

## Reference(s):

- [Provider CLI guide](artifact/references/provider-cli.md)
- [Image model flags reference](artifact/references/model-flags.md)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Image files, Shell commands, Image-editing prompts, Guidance]

**Output Format:** [Edited image files (typically JPEG) with shell commands and prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the original image and a high-resolution photo of the same product as references; output format and quality depend on the selected provider and command options.]

## Skill Version(s):

1.0.32 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
