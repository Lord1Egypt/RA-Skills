## Description: <br>
Deploy and interact with Ponzu token launchpad: presales, DEX swaps, and LP farming on Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YuzuKyouma](https://clawhub.ai/user/YuzuKyouma) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate SDK, viem, or MCP-based guidance for deploying Ponzu ERC-20 launches, reading contract state, buying or selling through PonzuSwap, and managing LP farming workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signed Ponzu actions can spend real ETH or deploy contracts when a private key is configured. <br>
Mitigation: Use a dedicated wallet with only the funds needed, test on Sepolia before mainnet, and omit PONZU_PRIVATE_KEY for read-only access. <br>
Risk: NFT metadata hosted through Pinata, Arweave, or HTTPS services may be visible to or retained by those services. <br>
Mitigation: Choose the metadata host deliberately, keep Pinata credentials secure, and avoid publishing private or sensitive metadata. <br>
Risk: Incorrect network or RPC configuration can send transactions to an unintended Ethereum network. <br>
Mitigation: Set PONZU_NETWORK and PONZU_RPC_URL explicitly and verify contract addresses before signing transactions. <br>


## Reference(s): <br>
- [Ponzu homepage](https://ponzu.app) <br>
- [ClawHub release page](https://clawhub.ai/YuzuKyouma/ponzu-ethereum) <br>
- [Ethereum mainnet RPC directory](https://chainlist.org/chain/1) <br>
- [Sepolia RPC directory](https://chainlist.org/chain/11155111) <br>
- [Ponzu MCP package](https://www.npmjs.com/package/@ponzu_app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript and JSON code blocks plus inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, RPC, network, contract address, metadata hosting, and MCP configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
