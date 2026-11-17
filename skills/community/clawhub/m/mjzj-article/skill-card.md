## Description:

帮助代理搜索卖家之家跨境电商资讯，并在授权后发布 HTML 资讯文章和图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to search MJZJ cross-border e-commerce articles, inspect their own author and article records, and publish authorized HTML articles through MJZJ APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing flow can fetch and re-upload external images and publish articles or media under the user's MJZJ account.

Mitigation: Use only trusted content and image sources, require explicit confirmation before publishing or re-hosting images, and validate image URL, network, size, redirect, and MIME properties before download or upload.

Risk: Private and publishing endpoints send the user's MJZJ_API_KEY to MJZJ APIs.

Mitigation: Store the key only in the configured skill environment, rotate it if exposed, and replace it from the MJZJ user center when authorization fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-article)
- [MJZJ homepage](https://mjzj.com)
- [MJZJ API key settings](https://mjzj.com/user/agentapikey)
- [MJZJ author application](https://mjzj.com/user/authorapplication)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with MJZJ API request examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private and publishing operations require MJZJ_API_KEY; public article search can run without a token.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
