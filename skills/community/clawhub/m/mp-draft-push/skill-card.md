## Description:

将现成的文章 HTML 和可选封面图上传到微信公众号，并创建草稿供发布前检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhongchen](https://clawhub.ai/user/wuhongchen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to publish already prepared WeChat Official Account article content into the draft box, including optional cover image upload, before manually reviewing and publishing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WeChat Official Account credentials that can create drafts and upload materials.

Mitigation: Load credentials only for the publishing command, restrict .env file permissions, and rotate the AppSecret if it has been broadly exported.

Risk: Unpublished article HTML and cover images may be handled through temporary files.

Mitigation: Treat unpublished content as sensitive and review temporary-file handling before using the skill with confidential drafts.

Risk: Created drafts still require editorial and account-owner review before public publication.

Mitigation: Open the WeChat Official Accounts backend after draft creation and verify images, formatting, title, and digest before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhongchen/skills/mp-draft-push)
- [Publisher profile](https://clawhub.ai/user/wuhongchen)
- [Project homepage](https://github.com/bbwdadfg/wechat-ai-publisher)
- [WeChat Official Accounts admin console](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON construction examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates WeChat draft metadata and returns user-facing draft status, including title, digest, and draft media ID when successful.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
