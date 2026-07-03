## Description: <br>
Multi Protocol Bridge helps agents use AgentPMT-hosted HTTP tool calls for FTP and FTPS file operations, SSH command execution, and MQTT or MQTTS message publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill when an agent needs to transfer or delete files over FTP or FTPS, run remote SSH commands, or publish MQTT messages through AgentPMT-hosted tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad remote access to FTP, SSH, and MQTT systems through an external gateway. <br>
Mitigation: Install it only when that access is intentional, scope calls to explicit hosts and paths, and require human review for SSH commands, uploads, deletes, and retained MQTT publishes. <br>
Risk: Connection URLs and options may contain sensitive credentials such as passwords or SSH private keys. <br>
Mitigation: Prefer dedicated credential mechanisms when available, avoid putting secrets in prompts or logs, and use only the minimum credentials needed for each task. <br>
Risk: Unencrypted protocol schemes can expose file transfer or messaging data. <br>
Mitigation: Prefer FTPS, SSH key authentication with known-host verification, and MQTTS with TLS for sensitive systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/multi-protocol-bridge) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/multi-protocol-bridge) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [Local Action Schema](schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples and remote tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports FTP upload, download, list, and delete operations; SSH command execution; and MQTT publish operations through AgentPMT-hosted calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
