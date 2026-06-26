## Description: <br>
PingCode research and development management platform API integration for querying work items, generating weekly reports, and managing project progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anytao](https://clawhub.ai/user/anytao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and project leads use this skill to inspect PingCode projects and work items, generate project status reports, and update selected work-item fields through the PingCode Open API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update script can change live PingCode work items. <br>
Mitigation: Require user approval before write operations and verify the exact work-item ID and fields before execution. <br>
Risk: PingCode client credentials and token request URLs may be exposed through terminal, agent, proxy, or request logs. <br>
Mitigation: Use a narrowly scoped PingCode application, keep credentials in environment variables, avoid logging secrets or token URLs, and rotate credentials after suspected exposure. <br>
Risk: Broad PingCode application scopes could give the skill more access than the intended project workflow needs. <br>
Mitigation: Configure the PingCode application with the smallest data access scope that supports the intended read or update tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anytao/pingcode-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/anytao) <br>
- [PingCode API Reference](references/api_docs.md) <br>
- [PingCode Open API](https://open.pingcode.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, optional JSON, Markdown reports, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PINGCODE_CLIENT_ID and PINGCODE_CLIENT_SECRET environment variables; update operations can modify live PingCode work items.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
