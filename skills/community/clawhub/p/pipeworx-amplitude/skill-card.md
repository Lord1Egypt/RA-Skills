## Description: <br>
Retrieve and analyze user events, active counts, retention, and profiles in Amplitude with detailed date-range and granularity options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to the Pipeworx Amplitude MCP gateway for querying event counts, active users, retention metrics, user search, and user activity timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route sensitive Amplitude user profile and activity data through an external Pipeworx gateway without enough disclosure about access scope or data handling. <br>
Mitigation: Install only after verifying gateway trust, Amplitude authentication, workspace scope, permission scope, logging and retention practices, and revocation procedures. <br>
Risk: User search and activity queries may expose individual user data. <br>
Mitigation: Use least-privilege Amplitude access and query individual users only when there is a legitimate authorization basis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-amplitude) <br>
- [Pipeworx Amplitude MCP endpoint](https://gateway.pipeworx.io/amplitude/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls] <br>
**Output Format:** [Markdown with JSON MCP server configuration and MCP tool descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tools can return Amplitude event counts, active-user counts, retention metrics, matching user profiles, and user activity timelines for requested date ranges or users.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
