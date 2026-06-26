## Description: <br>
Search and retrieve detailed information about board games, including popular titles, player counts, playtime, ratings, prices, and descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search board games, inspect details for a selected game, and find currently popular games through the Pipeworx boardgames MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Board-game search queries are routed through the Pipeworx gateway rather than directly to the underlying board-game data source. <br>
Mitigation: Avoid sending sensitive private information in game-search prompts. <br>
Risk: Returned board-game details such as ratings, prices, and popularity may be incomplete or stale. <br>
Mitigation: Review important purchase or publication decisions against an authoritative current source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-boardgames) <br>
- [Pipeworx boardgames MCP gateway](https://gateway.pipeworx.io/boardgames/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration] <br>
**Output Format:** [Markdown or text responses with board-game fields returned from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include game titles, IDs, year, player count, playtime, rating, price, descriptions, and popularity rankings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
