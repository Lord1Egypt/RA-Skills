## Description: <br>
Secret redaction MCP server for OpenClaw agents that helps prevent API keys, database credentials, SSH keys, emails, IPs, JWTs, and other sensitive values from leaking to LLM providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a local secret-redaction layer when reading, writing, scanning, or proxying content that may contain credentials. It supports MCP setup, command guarding, file and directory scanning, audit reporting, canary tokens, and optional outbound LLM API proxying. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect sensitive local files while scanning or redacting credentials. <br>
Mitigation: Limit scans to intended directories and review the Pastewatch upstream project before use. <br>
Risk: The optional persistent proxy can continuously inspect outbound LLM API traffic. <br>
Mitigation: Enable the proxy only when continuous inspection is intended and configure upstream routing and audit logging deliberately. <br>
Risk: Vault keys and audit logs may expose sensitive operational metadata if poorly protected. <br>
Mitigation: Protect vault keys and audit logs with appropriate file permissions, access controls, and retention practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppiankov/pastewatch-mcp) <br>
- [Pastewatch project](https://github.com/ppiankov/pastewatch) <br>
- [Agent-Native CLI Convention](https://ancc.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pastewatch-cli and mcporter binaries; can produce redacted text, scan results, audit reports, and setup guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
