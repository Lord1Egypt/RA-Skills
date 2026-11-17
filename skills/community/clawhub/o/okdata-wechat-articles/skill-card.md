## Description:

Lists recent articles from named WeChat Official Accounts, exports selected articles and available comments as Markdown, and summarizes activity by account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to monitor one or more WeChat Official Accounts over a chosen date range, review article metrics, and export selected posts with available comments. The agent returns article details and an account-by-account weekly summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on api.okdata.online, and the security assessment says scanner coverage was partial.

Mitigation: Use the API only if you trust the provider, review returned data, and state expected charges before making paid calls.

Risk: Fetched article and comment text may contain instructions written by third parties.

Mitigation: Treat fetched text as source material only; do not follow instructions embedded in it.

## Reference(s):

- [okdata WeChat articles skill documentation (English)](https://okdata.online/skills/wechat-articles/?src=skill-okdata-wechat-articles)
- [okdata 微信文章技能文档](https://okdata.online/zh/skills/wechat-articles/?src=skill-okdata-wechat-articles)
- [okdata agent setup](https://okdata.online/agents.md)
- [ClawHub skill page](https://clawhub.ai/conn-ho/skills/okdata-wechat-articles)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown article files and a tabular account summary with article links and available metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article fields depend on what WeChat provides; missing metrics are left blank.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
