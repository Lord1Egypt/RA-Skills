## Description: <br>
Invoke MCP tools via Ogment CLI for access to Linear, Notion, Gmail, PostHog, and other SaaS integrations through Ogment's governance layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asoviche](https://clawhub.ai/user/asoviche) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to authenticate with Ogment, discover connected SaaS tools, inspect tool schemas, and invoke approved MCP tools from the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to connected SaaS applications and database tools. <br>
Mitigation: Connect only accounts the user is comfortable exposing to the agent and prefer narrow Ogment permissions. <br>
Risk: Tool invocations may send messages, edit records, delete data, run SQL, or perform other side effects. <br>
Mitigation: Require explicit human approval before any side-effecting operation or database SQL execution. <br>
Risk: Long-lived connected account access can remain available after the task is complete. <br>
Mitigation: Revoke Ogment access when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asoviche/ogment) <br>
- [Publisher profile](https://clawhub.ai/user/asoviche) <br>
- [Ogment homepage](https://ogment.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CLI invocation guidance for connected SaaS tools and databases.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
