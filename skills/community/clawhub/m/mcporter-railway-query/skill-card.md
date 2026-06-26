## Description: <br>
Queries Chinese railway ticket information through the mcporter CLI for G/D/C trains, schedules, seat availability, and route planning with date, time, train-type, and sorting filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lancenas](https://clawhub.ai/user/Lancenas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to look up Chinese railway station codes, train schedules, ticket availability, and filtered route options through a user-configured 12306 MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Railway route, station, date, and time query details are sent through the user's configured mcporter CLI and 12306 MCP server. <br>
Mitigation: Install only trusted mcporter and MCP server configurations, and review ~/.mcporter/mcporter.json before running the helper scripts. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/Lancenas/mcporter-railway-query) <br>
- [Query examples](references/query-examples.md) <br>
- [Station codes](references/station-codes.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and text, JSON, or CSV query results from mcporter.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only lookup helper; outputs depend on the user's mcporter CLI and configured 12306 MCP server.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
