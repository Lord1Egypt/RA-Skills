## Description: <br>
OpenClaw JSON Toolkit helps agents format, validate, diff, query, transform, and generate schemas for bounded JSON inputs through a remote MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yedanyagamiai-cmd](https://clawhub.ai/user/yedanyagamiai-cmd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to inspect and reshape JSON payloads, compare configuration changes, extract nested values, and generate draft-07 JSON Schema from samples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JSON content is sent to the listed remote MCP server for processing. <br>
Mitigation: Avoid secrets, credentials, private customer records, and regulated data unless the publisher and stated no-storage policy are trusted. <br>
Risk: Large or unbounded JSON payloads may exceed the artifact's stated edge-worker limits. <br>
Mitigation: Split JSON over 1MB into smaller bounded chunks before processing. <br>
Risk: Generated schemas, diffs, or transforms may be incomplete for production contracts if sample data is not representative. <br>
Mitigation: Review generated output against real API requirements before adopting it in production workflows. <br>


## Reference(s): <br>
- [OpenClaw MCP Servers Homepage](https://github.com/yedanyagamiai-cmd/openclaw-mcp-servers) <br>
- [OpenClaw JSON Toolkit MCP Endpoint](https://json-toolkit-mcp.yagami8095.workers.dev/mcp) <br>
- [ClawHub Skill Listing](https://clawhub.ai/yedanyagamiai-cmd/openclaw-json-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON results and text diagnostics returned through MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes text JSON inputs; artifact guidance recommends bounded payloads and no secret, credential, private customer, or regulated data unless the publisher and no-storage policy are trusted.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
