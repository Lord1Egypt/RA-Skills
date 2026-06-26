## Description: <br>
Search, retrieve, and get trending anime details including title, episodes, status, score, genres, and synopsis via the AniList GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search AniList for anime titles, retrieve anime details by ID, and review currently trending anime through a remote MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a remote third-party MCP gateway whose runtime behavior is not locally reviewable from this artifact. <br>
Mitigation: Use it for ordinary anime lookups only, avoid sending private or sensitive text, and review returned results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-anilist) <br>
- [AniList MCP gateway](https://gateway.pipeworx.io/anilist/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with anime lookup results and MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns anime metadata such as titles, episode counts, status, scores, genres, synopses, duration, and popularity ranking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
