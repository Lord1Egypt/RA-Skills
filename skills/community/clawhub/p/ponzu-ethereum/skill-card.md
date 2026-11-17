## Description:

Deploy and interact with Ponzu token launchpad for presales, DEX swaps, and LP farming on Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzukyouma](https://clawhub.ai/user/yuzukyouma)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to deploy Ponzu ERC-20 launchpad flows and interact with presales, token launches, swaps, LP staking, rewards, and contract state on Ethereum mainnet or Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide wallet-signing transactions involving real funds.

Mitigation: Use a dedicated low-value wallet, omit PONZU_PRIVATE_KEY for read-only access, and test on Sepolia before mainnet.

Risk: The optional MCP setup runs an external npm package and may receive signing authority when PONZU_PRIVATE_KEY is configured.

Mitigation: Pin and audit npm or MCP package versions before granting access to private keys.

Risk: Unsafe zero minimum-output examples can expose users to avoidable slippage or poor execution.

Mitigation: Replace zero minimum-output values with quote-based slippage limits before signing transactions.

Risk: Transactions depend on the configured Ethereum RPC endpoint.

Mitigation: Explicitly set and validate PONZU_RPC_URL for the intended network before broadcasting transactions.

## Reference(s):

- [Ponzu homepage](https://ponzu.app)
- [ClawHub skill page](https://clawhub.ai/yuzukyouma/skills/ponzu-ethereum)
- [Mainnet RPC reference](https://chainlist.org/chain/1)
- [Sepolia RPC reference](https://chainlist.org/chain/11155111)
- [@ponzu_app/mcp on npm](https://www.npmjs.com/package/@ponzu_app/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Ethereum contract addresses, environment variable requirements, and wallet safety guidance.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
