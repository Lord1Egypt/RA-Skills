## Description:

大宗商品行业资讯查询技能。用于查询钢铁、有色、能源化工等行业的动态新闻、市场快讯、政策变化、企业消息、价格异动分析、供需事件等资讯信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyb92](https://clawhub.ai/user/wyb92)

### License/Terms of Use:

MIT-0

## Use Case:

Commodity market analysts, researchers, and industry users use this skill to search Mysteel information about steel, non-ferrous metals, energy chemicals, policy changes, company activity, price movement causes, and supply-demand events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's documented setup can lead users to store a real Mysteel API token in a plaintext markdown file inside the skill directory.

Mitigation: Prefer an environment variable or protected secret store; if references/api_key.md is used, keep it out of source control and shared workspaces and restrict local file permissions.

Risk: User query text and the API token are sent to Mysteel's API during searches.

Mitigation: Review queries for sensitive content before execution and only use credentials intended for this third-party API.

## Reference(s):

- [API Reference](references/api_reference.md)
- [Mysteel Info Search API endpoint](https://mcp.mysteel.com/mcp/info/ai-search/search)
- [ClawHub skill page](https://clawhub.ai/wyb92/skills/mysteel-infosearch)
- [Publisher profile](https://clawhub.ai/user/wyb92)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON response data or Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Mysteel API token and sends query text to the Mysteel API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
