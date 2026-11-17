## Description:

Validates Lean Solidity IR, generates Solidity, compiles ABI and bytecode, encodes calls, and runs offline EVM simulations through AgentPMT-hosted remote tool calls.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fetch Lean templates, validate advanced Lean Solidity IR, generate Solidity, compile deployable artifacts, encode ABI calls, and simulate contract behavior before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The schema allows submitting a raw wallet private key and other sensitive blockchain materials to a remote service.

Mitigation: Do not provide real private keys, mnemonics, signatures, account secrets, or payment headers; prefer fromAlias or test-only throwaway keys unless transfer handling has been reviewed and approved.

Risk: Remote calls may expose proprietary contract logic or Lean source to AgentPMT-hosted infrastructure.

Mitigation: Keep inputs scoped to the minimum needed and submit proprietary contract logic only after approving the data transfer and handling model.

Risk: The artifact describes the Lean-to-Solidity mapping as proof of concept and not exhaustive.

Mitigation: Review generated Solidity, compile outputs, and simulation behavior carefully, and require normal smart-contract testing and security review before deployment.

Risk: The setup path includes unpinned npx installation commands.

Mitigation: Verify the package, source, and version before using npx-based setup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/lean-proof-to-solidity-smart-contract-generator)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/lean-proof-to-solidity-smart-contract-generator)
- [Action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and generated Solidity, ABI, bytecode, calldata, diagnostics, or simulation result content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote responses are treated as authoritative for each tool call; generation jobs may require polling by task id.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
