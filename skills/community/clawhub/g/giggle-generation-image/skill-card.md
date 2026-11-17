## Description:

Supports text-to-image and image-to-image generation through Giggle's Generation API, including reference images, model selection, aspect ratio, and resolution controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit text-to-image or image-to-image generation jobs, then query task status and receive generated image links when ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, base64 image content, asset IDs, and the Giggle API key are sent to giggle.pro.

Mitigation: Use only data intended for Giggle processing, avoid sensitive private images or internal signed URLs, and protect the API key as a secret.

Risk: Returned image links may be signed URLs that grant access to generated assets.

Mitigation: Share returned links only with intended recipients and avoid reposting signed links broadly.

Risk: The skill depends on Python requests installed from a version range.

Mitigation: Pin dependency versions before installation when reproducibility or supply-chain controls are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/giggle-generation-image)
- [Giggle service](https://giggle.pro/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages, JSON task state, and signed image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GIGGLE_API_KEY and may return asynchronous task IDs before images are ready.]

## Skill Version(s):

0.0.10 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
