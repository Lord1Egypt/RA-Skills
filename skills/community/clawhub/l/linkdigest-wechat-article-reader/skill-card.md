## Description:

Reads public WeChat articles through LinkDigest and returns article text, image OCR, key points, metadata, and extracted links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and researchers use this skill to extract the text, image captions and OCR, key points, and links from a supplied public WeChat article for review or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted article links are processed remotely, and text results may be cached and reused for later requests to the same article.

Mitigation: Submit only public, non-sensitive articles; do not submit private, internal, or login-only links.

Risk: Full article and image processing can consume paid API credits.

Mitigation: Check coverage and credit usage, and set a maximum credit budget before processing long articles.

Risk: The bundled helper accepts broader LinkDigest inputs than the WeChat-only skill description suggests.

Mitigation: Limit inputs to intended public mp.weixin.qq.com article links.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jackchew7143/skills/linkdigest-wechat-article-reader)
- [LinkDigest documentation](https://linkdigest.dev/zh/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown by default; structured JSON on request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports article metadata, per-image text, links, reading coverage, and credit usage; without an API key, the helper offers only a limited summary.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
