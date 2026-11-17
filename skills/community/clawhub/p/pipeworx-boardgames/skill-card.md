## Description:

Search and retrieve detailed information on board games, including popular titles, player count, playtime, rating, price, and descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting board-game shoppers, players, or reviewers can use this skill to search for games, retrieve full details by game ID, and surface currently popular titles for comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Board-game search terms and game IDs are sent to the configured Pipeworx gateway.

Mitigation: Install only where that remote-service data sharing is acceptable, and avoid submitting sensitive internal context as search terms.

Risk: Returned game descriptions and metadata are remote content.

Mitigation: Review important results before relying on them for purchasing, publishing, or user-facing recommendations.

Risk: An MCP client with broad permissions may expose more remote functionality than the documented board-game lookup tools.

Mitigation: Use a client configuration that limits the server to the documented search_games, get_game, and hot_games tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-boardgames)
- [Pipeworx Boardgames MCP endpoint](https://gateway.pipeworx.io/boardgames/mcp)

## Skill Output:

**Output Type(s):** [Text, Structured data, Configuration]

**Output Format:** [MCP tool responses with board-game search results and game details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include titles, years, player counts, playtime, ratings, prices, descriptions, and game IDs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
