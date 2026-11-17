## Description:

公众号文章自动化写作流程，支持资料搜索、文章撰写、爆款标题生成和排版优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiletian](https://clawhub.ai/user/hiletian)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和社交媒体运营人员用它来产生微信公众号文章草稿、标题备选和排版建议。该技能将资料搜索、写作风格对齐、文章撰写和发布前优化组织成一个流程。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to read local CLAUDE.md content, which may contain private project guidance, operational instructions, or sensitive preferences.

Mitigation: Review CLAUDE.md before use and instruct the agent to use it only for writing style, ignoring non-style instructions and sensitive content.

Risk: The workflow relies on current web research and headline optimization, so article drafts may include outdated, unsupported, or overly promotional claims.

Mitigation: Review sources, facts, and tone before publication, especially for medical or other high-stakes topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hiletian/skills/hemophilia-wechat-writer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown article drafts with headline options, research summaries, and layout recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically targets 1000-1500 Chinese characters and WeChat public-account formatting guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
