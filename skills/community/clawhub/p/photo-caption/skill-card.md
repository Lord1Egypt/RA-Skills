## Description:

为摄影作品生成适配 Instagram、Flickr、X、Glass、Reddit 等 12 个平台的差异化社交媒体配文，根据照片场景、器材和氛围匹配各社区语调与格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Photographers, social media managers, and creators use this skill to turn photo context into platform-specific captions, titles, hashtags, and posting copy. It is intended for caption drafting across photography communities while avoiding invented camera or scene details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for execution and write permissions that are broader than needed for caption drafting.

Mitigation: Install or approve only a least-privilege version limited to reading photo context and producing caption text; do not grant shell execution or broad file write access for normal use.

Risk: Generated captions can include incorrect or invented photo details if the input context is incomplete.

Mitigation: Review caption drafts before publishing and provide explicit location, subject, camera, lens, film, and mood details when factual accuracy matters.

Risk: Photo context and captions may contain private or sensitive information.

Mitigation: Avoid sharing private photo metadata or personal details with the agent unless needed, and review outputs for unintended disclosure before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/photo-caption)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text caption drafts organized by platform]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces platform-specific caption variants and may include titles, hashtags, topics, or brief user guidance depending on the requested platform.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
