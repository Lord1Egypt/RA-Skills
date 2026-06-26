## Description: <br>
Search Star Wars characters, planets, starships, and films with detailed attributes from the original six movies via the Star Wars API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query a hosted SWAPI MCP endpoint for Star Wars people, planets, starships, and film details without configuring local services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to the third-party Pipeworx SWAPI MCP gateway. <br>
Mitigation: Use the skill only for non-sensitive Star Wars lookups and avoid entering secrets, personal information, or proprietary data. <br>
Risk: Hosted lookup results may be unavailable or differ from user expectations for Star Wars data. <br>
Mitigation: Treat returned data as third-party API output and verify important facts before using them in user-facing or durable materials. <br>


## Reference(s): <br>
- [Pipeworx swapi on ClawHub](https://clawhub.ai/brucegutman/pipeworx-swapi) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [Pipeworx SWAPI MCP endpoint](https://gateway.pipeworx.io/swapi/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns text guidance for using MCP tools and hosted Star Wars API lookup results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
