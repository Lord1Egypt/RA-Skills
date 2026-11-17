## Description:

帮助代理围绕技术新闻链接或主题进行实时调研，产出有观点、带真实引用和截图素材的公众号或博客文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, analysts, and content teams use this skill to turn current AI or technology news topics into researched Chinese blog or WeChat-style articles with source citations, representative reactions, analysis, and screenshot assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to perform live web research, where sources or quoted reactions may be incorrect, stale, or unverifiable.

Mitigation: Verify factual claims and quotations against primary or reputable sources, and remove any claim or quote that cannot be confirmed.

Risk: The skill suggests unpinned npx commands, which can run changing tool versions.

Mitigation: Use pinned, trusted, preinstalled tool versions where possible and review commands before execution.

Risk: The skill asks agents to browse and screenshot arbitrary URLs, which could capture private or logged-in content.

Mitigation: Restrict screenshots to trusted public sources, avoid authenticated pages, and review generated images before publication.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/jessy-huang/skills/news-insight-writer)
- [ClawHub publisher profile](https://clawhub.ai/user/jessy-huang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown article with source citations and linked screenshot assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a generated-images folder containing screenshots referenced by the article.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
