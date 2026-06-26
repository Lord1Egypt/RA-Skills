## Description: <br>
OpenClaw FEISHU MCP configures OpenClaw agents to use Feishu MCP tools for reading, creating, updating, and table-editing cloud documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cry779](https://clawhub.ai/user/cry779) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure an agent for Feishu document workflows, including reading documents, extracting or updating tables, creating documents, and appending or replacing document content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configuration example includes a live-looking app secret that users might copy into their OpenClaw configuration. <br>
Mitigation: Do not use the embedded secret; create scoped Feishu app credentials, store them securely, and rotate any credential that may have been exposed. <br>
Risk: The skill enables agent-initiated document write, replace, append, create, and table update actions in Feishu. <br>
Mitigation: Require explicit user confirmation before document-changing actions and restrict the Feishu app permissions to the minimum required scope. <br>
Risk: The configured MCP endpoint and referenced Feishu OpenClaw plugin determine how document actions are executed. <br>
Mitigation: Verify the MCP endpoint and plugin source before installation or production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with JSON configuration and tool invocation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu document tokens, table block identifiers, app credentials, and markdown document content supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
