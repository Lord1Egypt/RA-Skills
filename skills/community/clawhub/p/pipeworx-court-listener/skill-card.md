## Description: <br>
Search U.S. court opinions and dockets by keyword, and retrieve specific court opinions by CourtListener ID without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal researchers, journalists, developers, and agents use this skill to search public U.S. court opinions or dockets and retrieve known CourtListener opinions during public court-record research. <br>

### Deployment Geography for Use: <br>
Global, for research into U.S. court records <br>

## Known Risks and Mitigations: <br>
Risk: Court-record queries are routed through a third-party Pipeworx-hosted MCP gateway and may include sensitive legal or personal information. <br>
Mitigation: Use for public court-record research, and avoid privileged legal strategy, confidential case information, or sensitive personal details unless you trust the gateway and its privacy practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-court-listener) <br>
- [Pipeworx CourtListener MCP gateway](https://gateway.pipeworx.io/court-listener/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses, with MCP server configuration JSON when setup is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes court-record queries through a third-party Pipeworx-hosted MCP gateway; no local code or privileged access is shown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
