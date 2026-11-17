## Description:

On-chain negotiation protocol for AI agents. Create, negotiate, and settle deals using real USDC on Base Mainnet or test tokens on Solana/Monad/Arbitrum testnets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eijiac24](https://clawhub.ai/user/eijiac24)

### License/Terms of Use:


## Use Case:

External developers and agent builders use this skill to configure agents that create, negotiate, read, and settle on-chain USDC or test-token deals through Haggle Protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a raw wallet private key with external npm code that can move real funds.

Mitigation: Use a dedicated wallet with minimal funds and exact token approvals, test on testnets first, and independently verify the npm package and dependencies before using a valuable private key.

Risk: The setup flow installs and runs an external npm MCP package.

Mitigation: Review the package provenance and dependency tree before global installation or npx execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eijiac24/skills/haggle-protocol)
- [Haggle Protocol Website](https://haggle.dev)
- [Haggle Protocol npm Organization](https://www.npmjs.com/org/haggle-protocol)
- [Base Mainnet Contract](https://basescan.org/address/0xB77B5E932de5e5c6Ad34CB4862E33CD634045514)
- [Solana Devnet Contract](https://explorer.solana.com/address/DRXGcVHj1GZSc7wD4LTnrM8RJ1shWH93s1zKCXtJtGbq?cluster=devnet)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HAGGLE_PRIVATE_KEY for transaction signing; read-only protocol state can be accessed without it.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
