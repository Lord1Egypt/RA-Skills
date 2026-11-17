## Description:

Create complete WeChat Official Account viral articles from a user-provided title by researching high-view YouTube videos, confirming topic/outline with the user, writing professional content through self-iteration, and outputting both Markdown and HTML formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing operators use this skill to research current topics, generate WeChat Official Account article options, obtain user approval, and produce publication-ready Chinese article drafts. It also supports cover-image generation and optional WeChat draft or preview submission when the operator configures credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose WeChat or API secrets through examples, checks, logs, or copied configuration.

Mitigation: Remove or rotate exposed secrets, keep credentials in protected environment variables or local secret stores, and do not run credential-check commands that print secret values.

Risk: Publishing automation can submit WeChat drafts or previews before final review.

Mitigation: Disable automatic WeChat submission by default and require explicit operator approval before any draft, preview, or publish action.

Risk: Proxy and persistent-output workflows can expand exposure if used with untrusted content or hosts.

Mitigation: Require HTTPS and an allowlisted proxy host, isolate shared memory and output directories for untrusted research, and pin dependencies in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeffli2002/skills/jeffli-content-factory)
- [YouTube Research Checklist](artifact/references/youtube_research_checklist.md)
- [WeChat Viral Content Frameworks](artifact/references/wechat_viral_frameworks.md)
- [WeChat Format Rules](artifact/references/wechat-format-rules.md)
- [WeChat Publishing Rules](artifact/references/WECHAT_PUBLISH_RULES.md)
- [WeChat Cover Photo Guide](artifact/scripts/COVER_PHOTO_GUIDE.md)
- [Configuration Guide](artifact/CONFIGURATION.md)
- [API Key Setup Guide](artifact/API_KEY_SETUP.md)
- [Zhipu AI Platform](https://open.bigmodel.cn/)
- [WeChat Official Account Platform](https://mp.weixin.qq.com/)
- [WeChat Token API](https://api.weixin.qq.com/cgi-bin/token)
- [WeChat Draft API](https://api.weixin.qq.com/cgi-bin/draft/add)
- [WeChat Publish Submit API](https://api.weixin.qq.com/cgi-bin/freepublish/submit)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown and HTML article files, concise user-facing guidance, and optional shell commands for research, cover generation, and WeChat draft submission.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent article, image, and draft-publishing artifacts in configured output directories.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
