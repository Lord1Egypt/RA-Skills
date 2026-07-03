## Description: <br>
Use HuahuaDaily MCP to query portfolio, transactions, market data, screenshot imports, and send App-confirmed trade/import requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiye1997](https://clawhub.ai/user/baiye1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this MCP skill to let an agent access HuahuaDaily account data, fund and market information, screenshot import flows, and App-confirmed trade or import requests. It is intended for users who trust the connected agent with sensitive investment data and who can confirm write-sensitive actions in the HuahuaDaily App where required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP can read sensitive investment data, including portfolio values, transaction history, cloud sync data, and screenshot contents. <br>
Mitigation: Install only if the user trusts HuahuaDaily and the connected agent; configure a scoped, revocable Agent Token and avoid exposing more account detail than needed for the task. <br>
Risk: Trade and import workflows could be misunderstood as completed actions when the agent only sends requests. <br>
Mitigation: Require explicit user confirmation for trades and imports, and tell the user that the HuahuaDaily App confirmation page must be completed before the action takes effect. <br>
Risk: Community authorization, revocation, following, and community return synchronization are direct backend writes rather than App-confirmed requests. <br>
Mitigation: Call these community tools only after explicit user confirmation and describe them as directly effective actions, not pending App confirmations. <br>
Risk: Screenshot import tools can read and upload local files when given image paths. <br>
Mitigation: Use only user-provided image paths, avoid guessing or enumerating local files, and prefer base64 image inputs when the source path is uncertain. <br>
Risk: Unpinned Git installation examples can pull code that differs from the reviewed release. <br>
Mitigation: Prefer a pinned release or ClawHub install path over unpinned Git installation examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baiye1997/skills/huahua-daily) <br>
- [HuahuaDaily API base](https://api.huahuadaily.cn) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and shell or MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include portfolio, transaction, market, screenshot-import, report, community, and App-confirmation guidance based on authorized HuahuaDaily data.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
