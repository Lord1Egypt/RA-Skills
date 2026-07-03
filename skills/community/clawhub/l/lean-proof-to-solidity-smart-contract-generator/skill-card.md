## Description: <br>
Validates Lean Solidity IR, generates Solidity, compiles generated contracts to ABI and bytecode, encodes calls, and runs offline EVM simulations through AgentPMT-hosted remote tool calls. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to move from Lean Solidity IR toward generated Solidity artifacts, then validate, compile, encode calls, and simulate contract behavior before any deployment workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User code or sensitive blockchain credentials may be sent to hosted AgentPMT services. <br>
Mitigation: Use only code and artifacts approved for AgentPMT processing, avoid production private keys, and prefer test accounts, throwaway keys, redacted payloads, or secret-reference mechanisms. <br>
Risk: Generated Solidity, ABI, bytecode, calldata, or simulation results may be incomplete or unsuitable for production deployment. <br>
Mitigation: Validate Lean inputs, inspect generated Solidity, compile and simulate before use, and require independent review or audit before deploying contracts. <br>


## Reference(s): <br>
- [Action schema](schema.md) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/lean-proof-to-solidity-smart-contract-generator) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/lean-proof-to-solidity-smart-contract-generator) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and remote tool outputs such as Solidity code, ABI, bytecode, calldata, diagnostics, and simulation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include background task identifiers that must be polled before generated Solidity is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
