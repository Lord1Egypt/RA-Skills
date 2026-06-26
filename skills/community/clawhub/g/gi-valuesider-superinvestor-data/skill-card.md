## Description: <br>
Fetches Superinvestors' 13F portfolio holdings and buy/sell activity from ValueSider (valuesider.com). Use when the user asks for guru portfolio, 13F holdings, superinvestor positions, ValueSider data, or which stocks a fund/manager is buying or selling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to retrieve public ValueSider 13F portfolio holdings and buy/sell activity for named superinvestors or funds, then summarize the parsed results. Outputs should be treated as data reporting, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact ValueSider to retrieve public portfolio and activity pages. <br>
Mitigation: Use it only in environments where outbound requests to ValueSider are acceptable, and disclose ValueSider as the data source in user-facing summaries. <br>
Risk: The optional direct-fetch script depends on local Python packages and network behavior that may vary by environment. <br>
Mitigation: Run the scripts in an isolated Python environment and review or pin dependency versions before operational use. <br>
Risk: Parsed 13F holdings and activity can be mistaken for investment advice or fully current positions. <br>
Mitigation: Present results as public ValueSider-derived data reporting, include the reporting period when available, and avoid framing outputs as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laimiaohua/gi-valuesider-superinvestor-data) <br>
- [Publisher profile](https://clawhub.ai/user/laimiaohua) <br>
- [ValueSider](https://valuesider.com) <br>
- [ValueSider superinvestor list](https://valuesider.com/value-investors) <br>
- [ValueSider portfolio URL pattern](https://valuesider.com/guru/{guru_slug}/portfolio) <br>
- [ValueSider activity URL pattern](https://valuesider.com/guru/{guru_slug}/portfolio-activity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON parser output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Portfolio output includes summary and holdings; activity output includes activities with quarter, ticker, stock name, activity type, share change, portfolio percentage change, reported price, and portfolio percentage.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
