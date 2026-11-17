## Description:

一个提供实时《Old School RuneScape》玩家统计数据和排行榜数据的Model Context Protocol (MCP)服务器，支持多种游戏模式和玩家比较功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Old School RuneScape player statistics, leaderboards, activity rankings, and player comparisons through a third-party XiaoBenYang MCP API. The skill requires a user-provided API key before it can make requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a user-provided XiaoBenYang API key to a third-party API and stores that key in a plaintext .env file.

Mitigation: Use a disposable or limited-scope key, avoid committing the skill directory, and rotate or delete the key when uninstalling the skill.

Risk: Server security evidence flags copied Gaokao references that make the skill scope and provenance unclear.

Mitigation: Review the artifact before installation and confirm that the exposed tools and API identifiers match the intended OSRS use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/osrs-stat)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw API response data with success and message fields; requires an API key stored in a plaintext .env file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
