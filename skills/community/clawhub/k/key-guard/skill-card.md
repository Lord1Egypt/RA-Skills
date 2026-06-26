## Description: <br>
Key Guard routes API key checks, authenticated API calls, and key-bearing file reads or edits through a local MCP server so raw keys are not returned to the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[domjeff](https://clawhub.ai/user/domjeff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to keep API keys local while asking an agent to validate credentials, make authenticated HTTP requests, and inspect or edit scripts and configuration files that may contain keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local MCP server can read and use API keys, make authenticated outbound requests, and modify files. <br>
Mitigation: Restrict allowed key names, bind each key to trusted HTTPS domains, limit file operations to a specific workspace, and require explicit confirmation before any write or credentialed request. <br>
Risk: The security summary flags broad, under-scoped power over secrets, network requests, and file writes. <br>
Mitigation: Review and scan the skill before deployment, and install it only in environments where this local access model is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/domjeff/key-guard) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [mcp-config.json](mcp-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell and configuration snippets, JSON MCP tool results, and edited file content when writes are requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sensitive values are intended to remain local; outputs may include key names, masked placeholders, API responses, and non-secret file content.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
