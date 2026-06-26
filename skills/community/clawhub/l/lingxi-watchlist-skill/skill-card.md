## Description: <br>
国泰海通证券-灵犀自选管理 skill，支持查询自选股行情、添加、删除自选股，仅支持管理【我的自选】分组中的自选股。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtht-tech](https://clawhub.ai/user/gtht-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with an authorized 国泰海通/灵犀 brokerage account use this skill to view market data for their 【我的自选】 watchlist and to add or remove stocks from that group. Agents should present objective watchlist and quote information and obtain explicit confirmation before deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles persistent brokerage-account credentials and device identifiers. <br>
Mitigation: Install only from a trusted publisher, authorize through the official brokerage/灵犀 flow, manage device bindings there, and remove or protect gtht-entry.json when no longer needed. <br>
Risk: Watchlist add or delete actions can change the user's brokerage watchlist. <br>
Mitigation: Review proposed additions or deletions carefully and require explicit user confirmation before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtht-tech/lingxi-watchlist-skill) <br>
- [Publisher profile](https://clawhub.ai/user/gtht-tech) <br>
- [Gateway base URL](https://zx.app.gtja.com:8443/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and concise text with shell commands for authorization and watchlist operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user authorization before account-specific watchlist data or changes are available.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
