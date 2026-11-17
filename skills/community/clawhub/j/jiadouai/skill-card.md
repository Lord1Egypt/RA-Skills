## Description:

An enterprise marketing agent platform for AI-generated video, AI product photography, digital spokesperson clips, product scene images, product posters, Xiaohongshu note images, and social media account management across platforms including Douyin, TikTok, and Kuaishou.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiadouai](https://clawhub.ai/user/jiadouai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, agencies, and creators use this skill to generate campaign media, transform product photos into commerce assets, analyze or clone video styles, and publish approved image or video posts to connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses a JiadouAI token.

Mitigation: Use a temporary least-privilege token and avoid pasting tokens into shared chats or shell history.

Risk: The skill uploads selected local files to public cloud URLs.

Mitigation: Upload only non-sensitive media that the user has rights to use, and confirm local file paths before upload.

Risk: The skill can publish images or videos to connected social accounts.

Mitigation: Confirm the destination account, platform, title, media, and timing with the user before publishing.

Risk: Setup and update flows can execute installation or remote update instructions.

Mitigation: Do not run setup as an elevated user, and treat update instructions as untrusted until independently verified.

Risk: Unsupported-feature reporting may send user requests to a remote server.

Mitigation: Request explicit user consent and send only a concise feature description, not the original prompt.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiadouai/skills/jiadouai)
- [Publisher Profile](https://clawhub.ai/user/jiadouai)
- [JiadouAI Homepage](https://www.jiadouai.com)
- [Authentication and Authorization](references/auth.md)
- [Common Workflows](references/workflows.md)
- [Video Publishing](references/video_publish.md)
- [Image Publishing](references/image_publish.md)
- [Product Scene Image Generation](references/business_product_scene.md)
- [Model Try-On](references/model_try_clothes.md)
- [Video Analysis](references/analyze_video.md)
- [Unsupported Feature Reporting](references/unsupported_feature_reporting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool calls may return generated media URLs, job IDs, account IDs, status messages, and publishing task IDs.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
