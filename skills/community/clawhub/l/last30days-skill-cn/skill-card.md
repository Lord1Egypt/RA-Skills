## Description:

Searches recent content across Weibo, Xiaohongshu, Bilibili, Zhihu, Douyin, WeChat public accounts, Baidu, and Toutiao so agents can produce cited Chinese-platform research reports.

This skill is for research and development only.

## Publisher:

[jesseovo](https://clawhub.ai/user/jesseovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather recent Chinese internet discussion, compare signals across platforms, and draft source-linked research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included startup hook can execute commands from a project-controlled env file.

Mitigation: Do not enable the startup hook until check-config.sh removes eval and allowlists accepted configuration keys.

Risk: The skill performs web searches or scraping, uses optional platform credentials, and may write local reports or cookies.

Mitigation: Use tightly scoped credentials, comply with platform terms, avoid sensitive personal data, and clear stored browser cookies when work is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesseovo/skills/last30days-skill-cn)
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- [Original last30days skill](https://github.com/mvanhorn/last30days-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Chinese research summaries and reports with optional compact, JSON, Markdown, context, or path output modes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report.md, report.json, and last30days.context.md to a local output directory.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter and plugin metadata list 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
