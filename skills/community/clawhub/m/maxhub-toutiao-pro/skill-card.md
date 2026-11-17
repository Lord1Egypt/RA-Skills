## Description:

通过 MaxHub API（aconfig.cn）查询今日头条的文章、视频、评论、用户和热点数据，并辅助资讯分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

内容分析人员、研究者和开发者可用它查询授权范围内的今日头条内容与媒体号数据，辅助选题、舆情跟踪和互动分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests send the MaxHub API key and supplied identifiers, keywords, or URLs to the third-party service at aconfig.cn.

Mitigation: Use only authorized data, minimize personal information, and keep API credentials out of prompts and logs.

Risk: First-use and compliance workflows write confirmation and audit records under $HOME/.maxhub-skills/.compliance.

Mitigation: Keep this directory private and review its contents and retention as part of local data handling.

Risk: The documented npx installer does not pin a package version, and scanner coverage was partial.

Mitigation: Review the release source and installer version before installation, and inspect referenced local files when applying the workflow.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-toutiao)
- [MaxHub API](https://www.aconfig.cn)
- [Toutiao Open Platform](https://open.toutiao.com)
- [Recipe index](artifact/references/recipes/_index.md)
- [Endpoint whitelist](artifact/references/endpoints_whitelist.yaml)
- [Parameter and field mapping guide](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Natural-language summaries of retrieved data, with Markdown when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the API response and the identifiers or search terms provided.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
