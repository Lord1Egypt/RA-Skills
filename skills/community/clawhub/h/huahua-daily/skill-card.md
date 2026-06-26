## Description: <br>
Use HuahuaDaily MCP to query portfolio, transactions, market data, screenshot imports, and send App-confirmed trade/import requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiye1997](https://clawhub.ai/user/baiye1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External HuahuaDaily users and their agents use this MCP skill to read authorized portfolio, transaction, market, cloud sync, and screenshot data, then prepare trade or import requests for user confirmation in the app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive investment data, including portfolio values, transaction history, cloud sync snapshots, and screenshot contents. <br>
Mitigation: Install only for trusted agents, keep the Agent Token revocable and scoped, and limit responses to details needed for the user's question. <br>
Risk: The skill can initiate trade, import, screenshot upload, posting, community visibility, follow, and community return sync workflows. <br>
Mitigation: Require explicit user confirmation before these actions. Trades and imports still require final confirmation in HuahuaDaily, while community operations can take effect directly. <br>
Risk: Remote installation paths may run third-party code. <br>
Mitigation: Prefer the ClawHub or pip installation path over piping remote install scripts into a shell. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/baiye1997/huahua-daily) <br>
- [Publisher profile](https://clawhub.ai/user/baiye1997) <br>
- [HuahuaDaily API endpoint](https://api.huahuadaily.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-style MCP tool inputs and structured API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HuahuaDaily Agent Token; trade and import requests are sent for app confirmation, while community operations can write directly after explicit user confirmation.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release evidence, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
