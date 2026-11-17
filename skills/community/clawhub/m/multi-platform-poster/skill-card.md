## Description:

Adapts and publishes Markdown content across WeChat Official Accounts, Weibo, Zhihu, Xiaohongshu, and Douyin with scheduling and performance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing operators use this skill to adapt one source article into platform-specific posts, schedule publication, and review basic engagement results across Chinese social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may need access to social-media account credentials or OAuth/API permissions.

Mitigation: Confirm every account authorization screen, use the narrowest available scopes, and keep secrets in configured credential stores instead of chat.

Risk: Publishing or scheduling posts creates external side effects that may not be fully reversible on every platform.

Mitigation: Review generated platform-specific drafts and confirmation screens before approving publication or scheduled release.

Risk: Cross-platform adaptation can alter wording, truncate short posts, resize media, or add tags in ways that affect brand or compliance review.

Mitigation: Preview each platform version and require manual approval for sensitive, regulated, or brand-critical content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daimingvip-a11y/skills/multi-platform-poster)
- [ClawHub Multi-Platform Poster Documentation](https://clawhub.ai/docs/multi-platform-poster)
- [WeChat Official Account API Documentation](https://developers.weixin.qq.com/doc/offiaccount/)
- [Weibo Open Platform Wiki](https://open.weibo.com/wiki/)
- [Zhihu Developers](https://www.zhihu.com/developers)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-text posting plans, platform-specific drafts, confirmation prompts, status tables, and analytics summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled publishing plans, account-authorization requirements, platform links, and engagement metrics.]

## Skill Version(s):

0.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
