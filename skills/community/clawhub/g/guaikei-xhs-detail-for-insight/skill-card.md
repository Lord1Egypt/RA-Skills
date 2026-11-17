## Description:

根据小红书链接类型自动路由：笔记链接(explore/)走详情或评论、博主主页(user/profile/)走作品列表、短链(xhslink)按目标解析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, analysts, and agent operators use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator post lists for content research, competitor monitoring, trend analysis, and KOL screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and the GUAIKEI_API_TOKEN to Guaikei's API.

Mitigation: Use only public, non-sensitive inputs; confirm authorization for the API token and rotate it if it may have been exposed.

Risk: Input URLs can include xsec_token values and retrieved results are saved locally under logs/.

Mitigation: Treat xsec_token-bearing URLs as sensitive and clean up generated log files after use.

Risk: Server-side failures, rate limits, deleted content, or empty search results can prevent reliable data retrieval.

Mitigation: Check the returned status and error_code, retry only transient failures, and avoid presenting empty or failed responses as factual findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-detail-for-insight)
- [Guaikei API and token site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed scripts return structured JSON and may write JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supported tasks include keyword search, note detail retrieval, comment retrieval, and creator post retrieval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
