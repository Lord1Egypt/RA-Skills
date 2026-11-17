## Description:

一个提供实时和历史NBA数据的模型上下文协议服务器，包括球员统计、比赛得分、球队信息和高级分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NBA-data users can use this skill to query live and historical NBA scores, schedules, teams, players, standings, awards, and advanced statistics through XiaoBenYang API-backed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves the XiaoBenYang API key in plaintext in a workspace .env file.

Mitigation: Install only in workspaces where plaintext local credential storage is acceptable, and prefer short-lived or restricted API keys when possible.

Risk: The security scan reports mismatched gaokao/NBA configuration and an overridable credential-bearing API endpoint.

Mitigation: Review the configuration before use, confirm the intended XiaoBenYang API origin, and avoid running the skill in shared or sensitive workspaces until the mismatch is resolved.

Risk: Dependencies are declared with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before deployment in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/nba-stats)
- [XiaoBenYang API key source](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration guidance]

**Output Format:** [Markdown or text responses summarizing JSON API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY; tool calls return success, raw, and message fields before agent summarization.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
