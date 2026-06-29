## Description: <br>
Provides real-time and historical NBA data, including player statistics, game scores, team information, awards, and advanced analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer NBA data questions, resolve teams and players, retrieve scores and schedules, and summarize player, team, game, award, shooting, play-by-play, and advanced-statistics data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a third-party Xiaobenyang API key and stores it locally as XBY_APIKEY in a .env file. <br>
Mitigation: Install only if that credential handling is acceptable; review or delete the .env file when rotating keys and avoid sharing it. <br>
Risk: The scanner noted template residue in the documentation even though the inspected tools are NBA-focused. <br>
Mitigation: Review the skill text and available tools before deployment so users understand the actual NBA data workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/nba-stats) <br>
- [Xiaobenyang API key site](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration guidance] <br>
**Output Format:** [Markdown summaries with structured NBA data returned from tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xiaobenyang API key before data queries can be completed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
