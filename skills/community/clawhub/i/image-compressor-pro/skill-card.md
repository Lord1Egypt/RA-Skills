## Description:

Image Compressor presents a demo workflow for requesting compression of JPG, PNG, WebP, and GIF image URLs while describing file-size reduction and bulk support.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to ask an agent to optimize image URLs and return compression status details. The release should be treated as a demo until a real scoped compression, billing, and data-handling workflow is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release exposes a credential-like API key.

Mitigation: Remove and rotate the exposed key, then replace it with a nonfunctional placeholder before installation or redistribution.

Risk: Paid or external image processing is under-specified.

Mitigation: Clearly disclose whether image URLs or files leave the local environment and require explicit confirmation before any paid or external processing.

Risk: The artifact behaves like a demo rather than a complete compression and billing workflow.

Mitigation: Treat the skill as a demo until a real scoped compression and billing workflow is documented and provided.

## Reference(s):

- [Image Compressor ClawHub listing](https://clawhub.ai/loverun321/skills/image-compressor-pro)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with request status and image URL fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns demo compression status; no evidence confirms production image compression, billing, or file-handling behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
