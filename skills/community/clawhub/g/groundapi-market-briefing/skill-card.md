## Description: <br>
Generate A-share market briefings with indices, limit-up and limit-down pools, sector rotation, IPO calendar, anomaly signals, gold and forex macro data, trending topics, and a daily news digest powered by GroundAPI MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-focused agents use this skill to assemble A-share daily market briefings from GroundAPI market, macro, news, trend, and calendar data. The skill is suited for market summaries, post-market reviews, sector rotation checks, IPO calendar checks, and public-data news digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GroundAPI key and sends market, news, and any user-provided sector focus to GroundAPI. <br>
Mitigation: Configure only your own GROUNDAPI_KEY, treat it as a secret, and install the skill only when GroundAPI use is intended. <br>
Risk: Market and news briefings can become misleading if unavailable data is filled in or presented as investment advice. <br>
Mitigation: Skip failed data steps, disclose omissions, and preserve the skill's statement that the output is based on public data and is not investment advice. <br>


## Reference(s): <br>
- [GroundAPI homepage](https://groundapi.net) <br>
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/groundapi-market-briefing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown market briefing with tables, bullet lists, and concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language follows the user; failed data retrieval steps should be skipped and disclosed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
