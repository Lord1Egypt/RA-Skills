## Description:

全网持续收录每日公众号原创热门文章内容，向用户推送公众号原创热门文章；当用户需要获取全领域的公众号原创热门文章、或订阅每日原创热门文章推送时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users, WeChat editors, content planners, and operations teams use this skill to find original viral WeChat Official Account articles by category or date and to produce shareable ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and may expose the key if users mishandle configuration or logs.

Mitigation: Use a revocable, least-privilege REDFOX_API_KEY, keep it in environment configuration, and avoid placing it in prompts, code, generated files, or logs.

Risk: Network use is higher risk until TLS verification is fixed.

Mitigation: Review the skill before installation and avoid running it on untrusted networks unless TLS verification is corrected.

Risk: Generated HTML reports include remote article data and a CDN script that can execute in the browser.

Mitigation: Treat generated reports as untrusted, review them before sharing, and open them only in a controlled browser context.

Risk: The normal output includes a forced promotional message and subscription behavior is not clearly scoped.

Mitigation: Review deployment prompts and subscription handling so users understand what is optional and what data or schedule a subscription covers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/gzh-original-article-king)
- [Category mapping reference](references/category_mapping.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown article ranking tables, subscription prompt text, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; results are fetched from RedFox article data and may reflect the latest available snapshot rather than live read counts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
