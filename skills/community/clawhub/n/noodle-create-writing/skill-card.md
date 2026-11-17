## Description:

Generates food-focused social media articles for Douyin, Xiaohongshu, and Weibo by searching web content, extracting structured points, and formatting platform-specific posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyi0329-pixel](https://clawhub.ai/user/fyi0329-pixel)

### License/Terms of Use:

MIT

## Use Case:

Content creators, social media operators, and marketing teams use this skill to draft noodle and food-themed posts tailored to Douyin, Xiaohongshu, and Weibo. It is suited for generating platform-specific Markdown copy from a topic, keywords, and web search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled article topics and keywords can reach a shell command used for Tavily search.

Mitigation: Review before installation and replace shell command construction with an argument-array API or equivalent input-safe invocation.

Risk: Generated Weibo-style content can include giveaway or prize language.

Mitigation: Remove giveaway templates or require human approval before publishing promotional claims.

Risk: Food and health-benefit wording may produce unsupported health-effect claims.

Mitigation: Require source review and remove health claims unless they are explicitly authorized and substantiated.

Risk: The normal workflow saves raw search results and extracted data to disk.

Mitigation: Use dry-run for review workflows and make raw-data persistence opt-in before handling sensitive topics or sources.

Risk: Runtime behavior depends on external Tavily and npm packages.

Mitigation: Pin or verify dependencies and review the Tavily integration before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fyi0329-pixel/skills/noodle-create-writing)
- [Publisher Profile](https://clawhub.ai/user/fyi0329-pixel)
- [Tavily API](https://tavily.com)
- [OpenClaw Skill Development Guide](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown articles, plain-text article copies, and JSON source-data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Douyin, Xiaohongshu, Weibo, or all platforms; normal execution saves generated articles and source data unless dry-run is used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
