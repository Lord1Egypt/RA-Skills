## Description: <br>
MCP aggregation and Code Mode execution layer for token-efficient agent workflows that connects agents to Linear, GitHub, and other MCP servers through a single local endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cianbyrne1010](https://clawhub.ai/user/cianbyrne1010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage a local pctx MCP gateway, connect upstream Linear, GitHub, or other MCP servers, and batch MCP tool workflows through Code Mode TypeScript execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local MCP gateway can provide persistent agent access to connected tools and sensitive GitHub or Linear credentials. <br>
Mitigation: Use narrowly scoped tokens, connect only trusted upstream MCP servers, review the gateway configuration, and stop or remove the daemon when it is not needed. <br>
Risk: Adding untrusted npm, npx, or remote MCP endpoints can expand the agent's execution and data-access surface. <br>
Mitigation: Avoid untrusted packages and remote endpoints, review each MCP before adding it, and keep config backups so unsafe changes can be reverted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cianbyrne1010/pctx) <br>
- [pctx upstream project](https://github.com/portofcontext/pctx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local MCP tools and produce JSON-RPC responses through the pctx endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
