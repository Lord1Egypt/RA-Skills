## Description:

PostFlow AI helps manage AI-generated content across multiple social and content platforms with generation, SEO scoring, adaptation, scheduling, publishing notifications, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiyuan-studio](https://clawhub.ai/user/qiyuan-studio)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, marketers, and developers use this skill to generate, adapt, score, schedule, and manage social media and SEO content across platforms including Xiaohongshu, Douyin, Zhihu, WeChat, Weibo, X/Twitter, Reddit, and TikTok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises public social posting and publishing notifications, which can expose users to unintended or unauthorized publication.

Mitigation: Use test accounts first, require human review before publishing, and do not connect real social accounts until the approval flow and account permissions are clear.

Risk: The install path includes under-specified package and setup commands.

Mitigation: Run setup in a sandbox or disposable project environment, pin and verify dependencies, and avoid production API keys during installation and testing.

Risk: The security verdict is suspicious due to unclear scoping and safety details around publishing behavior.

Mitigation: Review the skill carefully before installation and deploy only after validating required permissions, webhook behavior, and publishing controls.

## Reference(s):

- [ClawHub PostFlow AI skill page](https://clawhub.ai/qiyuan-studio/skills/postflow-ai)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/SKILL.md)
- [Artifact manifest](artifact/manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured guidance with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform-specific content drafts, SEO review guidance, scheduling guidance, API integration notes, and deployment setup steps.]

## Skill Version(s):

1.3.0 (source: server release and artifact manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
