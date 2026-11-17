## Description:

小红书内容创作专家。输入主题/文章/视频链接，自动生成小红书图文（3:4比例，1080×1440 / 1242×1660 px），包含封面图、内页图和统一中文文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiletian](https://clawhub.ai/user/hiletian)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, knowledge bloggers, and health-content publishers use this skill to turn topics, articles, or videos into Xiaohongshu-ready image sets and a unified Chinese caption. It is especially oriented toward medical-health education, patient stories, and practical tutorial posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical-health claims in generated Xiaohongshu content may be inaccurate, incomplete, or unsuitable for publication without review.

Mitigation: Review health claims, add appropriate disclaimers, and confirm medical content before publishing.

Risk: User-provided article or video links may expose content the user did not intend to process.

Mitigation: Provide only links and source material that are appropriate for processing in the agent workspace.

Risk: Generated images are intended to be saved under the workspace output path.

Mitigation: Check generated files before sharing and remove any unwanted outputs from the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hiletian/skills/hemophilia-xiaohongshu-creator)
- [ClawHub publisher profile](https://clawhub.ai/user/hiletian)

## Skill Output:

**Output Type(s):** [text, markdown, images, guidance]

**Output Format:** [Markdown text with generated image links or workspace image paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 3:4 Xiaohongshu image sets, a shared caption, hashtags, and per-image topic notes.]

## Skill Version(s):

1.0.0 (source: server evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
