## Description:

基于 Model Context Protocol (MCP) 协议的全网热点趋势一站式聚合服务，支持实时更新和多数据源扩展。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and summarize current hot topics, rankings, and news from multiple Chinese and international content sources through XiaoBenYang MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a XiaoBenYang API key and stores it locally in plaintext.

Mitigation: Use a low-privilege key, avoid committing .env files, and rotate the key if it may have been exposed.

Risk: The API base URL can be configured, which can redirect API-key-bearing requests.

Mitigation: Review or restrict XBY_GAOKAO_BASE_URL before deployment.

Risk: The security summary reports that scripts/tools.py has invalid Python syntax and the package may not work until fixed.

Mitigation: Validate imports and run a syntax check before enabling the skill for users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/hot-news)
- [XiaoBenYang API key provider](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [Markdown or plain-text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; tool functions return success status, raw API payload, and a message.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
