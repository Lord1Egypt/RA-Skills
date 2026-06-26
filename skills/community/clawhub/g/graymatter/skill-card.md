## Description: <br>
Install and use GrayMatter as an OpenClaw skill that provides primary durable memory, shared object-graph state, and authenticated access to the live ValkyrAI schema via api-0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spaceghost69](https://clawhub.ai/user/spaceghost69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use GrayMatter to give an OpenClaw agent durable memory, shared graph context, and RBAC-scoped access to ValkyrAI organizational data. It is suited for teams that want agents to persist decisions, todos, context, artifacts, and preferences while working against a live business schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated access to live organizational data and permitted business actions. <br>
Mitigation: Use a dedicated least-privilege ValkyrAI account or per-request token, confirm RBAC scope before use, and require explicit user intent before entity creation or generic API calls. <br>
Risk: Credential reuse may cause an agent to operate under an existing workspace or account session. <br>
Mitigation: Confirm which Keychain or environment credentials are active before activation, avoid shared admin tokens, and rotate or revoke credentials that are no longer needed. <br>
Risk: Hosted GrayMatter queries and higher-order operations may consume account credits or create billable activity. <br>
Mitigation: Treat purchase, recharge, and credit-consuming operations as commercial actions that require clear user approval. <br>


## Reference(s): <br>
- [GrayMatter ClawHub Release](https://clawhub.ai/spaceghost69/graymatter) <br>
- [GrayMatter Architecture](docs/architecture.md) <br>
- [GrayMatter MCP Server](mcp-server/README.md) <br>
- [GrayMatter Privacy Policy](docs/privacy-policy.md) <br>
- [Portable MCP Memory Tool Contract](references/mcp/memory-tool-contract.v1.json) <br>
- [MCP Tool Contract](references/contracts/mcp/graymatter_mcp_tools_v1.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate authenticated API and MCP tool operations when the user grants credentials and intent.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
