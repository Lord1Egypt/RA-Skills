## Description:

Search Imagen Chat for relevant image URLs, use or download free watermarked images, and obtain temporary original-image links or download originals using an Imagen API key and credits. Supports numbered Markdown references and optional local selection and account setup. Not for image generation or catalog publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-cn](https://clawhub.ai/user/liu-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to find existing images on Imagen Chat for articles and other documents. It returns watermarked links or downloads and, when authorized, original-image links or downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence, citing undeclared analytics and image-request submission, including reported contact-detail transmission.

Mitigation: Review outbound data handling before installation; use generic search terms and keep optional keyword retention off unless explicitly opted in.

Risk: The scan fully inspected only 7 of 13 components, partly inspected the rest, and had degraded tool-misuse analysis.

Mitigation: Have a reviewer inspect the remaining components and outbound behavior before relying on the skill.

## Reference(s):

- [Imagen Search documentation](https://imagen.chat/skills/imagen-search)
- [Imagen Search on ClawHub](https://clawhub.ai/liu-cn/skills/imagen-search)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Image URLs, Image files]

**Output Format:** [Numbered Markdown with image links and source links; optional JSON manifests and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search candidates are metadata-based unless visually reviewed. Original-image links or downloads require an account, credits, and authorization.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
