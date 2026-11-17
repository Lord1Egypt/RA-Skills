## Description:

AI Image Upscaling API via HiResolutionPhotos sends low-resolution images for 4K or 8K upscaling and returns a secure private retrieval webpage for downloading the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[setdemos](https://clawhub.ai/user/setdemos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit local or web images to HiResolutionPhotos for AI upscaling, then provide the generated retrieval page link to the human user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to HiResolutionPhotos for processing.

Mitigation: Use only with images that are acceptable to send to that service; avoid confidential, regulated, or personal images unless its privacy terms meet your needs.

Risk: Upscaled outputs may be large files that are unsuitable for direct agent download.

Mitigation: Return the provided retrieval page URL to the human user rather than downloading the raw image through the agent.

Risk: The service enforces a 15-request-per-hour submission limit per IP.

Mitigation: Throttle submissions and stop retrying when rate-limit responses occur.

## Reference(s):

- [HiResolutionPhotos](https://hiresolutionphotos.com)
- [ClawHub skill page](https://clawhub.ai/setdemos/skills/hiresolutionphotos-upscaler)
- [Publisher profile](https://clawhub.ai/user/setdemos)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and a result retrieval URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; uploads PNG, JPG, or WebP images up to 10 MB; returns a retrieval page link instead of downloading the raw image.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
