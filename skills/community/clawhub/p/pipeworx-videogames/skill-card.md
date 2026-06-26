## Description: <br>
Browse and search free-to-play PC and browser games by platform, category, and sort order using data from the FreeToGame database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players, game scouts, and agents use this skill to browse free-to-play PC and browser games, retrieve detailed game profiles, and filter the catalog by platform, category, tags, popularity, or release date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries an external MCP endpoint for game catalog data. <br>
Mitigation: Use it only in environments where access to gateway.pipeworx.io is approved, and avoid sending sensitive information in game-search requests. <br>
Risk: Game listings, release dates, publisher details, URLs, and system requirements may be incomplete or outdated. <br>
Mitigation: Verify important game details against the linked game page or publisher before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-videogames) <br>
- [Pipeworx videogames MCP endpoint](https://gateway.pipeworx.io/videogames/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [MCP tool responses with game listings and details; setup is JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports platform, category, sort order, dot-separated tag filters, and game ID lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
