## Description: <br>
Chess.com player profiles, game stats, match archives, and leaderboards from the public API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, chess coaches, and community-tool builders use this skill to look up public Chess.com player profiles, ratings, game archives, and leaderboards. It supports public-data analysis and comparison without requiring Chess.com authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup requests are sent to Pipeworx's gateway. <br>
Mitigation: Use the skill for public Chess.com lookup data and avoid including private or unnecessary information in requests. <br>
Risk: The optional MCP setup downloads the current mcp-remote package unless a version is pinned. <br>
Mitigation: Pin the mcp-remote package version in MCP client configuration when repeatability or package supply-chain control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-chess) <br>
- [Pipeworx Chess pack](https://pipeworx.io/packs/chess) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON API responses, bash examples, and MCP client configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns public Chess.com profile, ratings, archive, and leaderboard data through the Pipeworx gateway; no Chess.com authentication is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
