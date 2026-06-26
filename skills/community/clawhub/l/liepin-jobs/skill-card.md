## Description: <br>
Liepin Jobs helps an agent search Liepin jobs, review or update resume data, and prepare job applications through the Liepin MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xllinbupt](https://clawhub.ai/user/xllinbupt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to search for roles on Liepin, inspect resume information, and prepare job applications. The skill should be used with explicit confirmation before submitting applications or changing resume data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a real Liepin account, including submitting job applications and editing resume data. <br>
Mitigation: Require clear manual confirmation before any application submission or resume update. <br>
Risk: The skill stores or uses a Liepin user token to access account and resume data. <br>
Mitigation: Protect the token, avoid exposing it in logs or chat, and install only when account access is acceptable. <br>
Risk: The generic MCP call command can invoke arbitrary Liepin tools. <br>
Mitigation: Avoid the generic call command unless the exact remote tool and arguments are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xllinbupt/liepin-jobs) <br>
- [Publisher profile](https://clawhub.ai/user/xllinbupt) <br>
- [Project homepage](https://github.com/xllinbupt/MCP2skill) <br>
- [Liepin MCP server configuration](https://www.liepin.com/mcp/server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable text or JSON, often summarized by the agent as Markdown tables and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live Liepin job, application, and resume data returned from the remote MCP service.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
