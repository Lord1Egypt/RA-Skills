## Description: <br>
Command-line interface guidance for creating, trading, swapping, transferring, and managing Mint Club V2 bonding curve tokens on the Base blockchain with wallet support and Uniswap integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebayaki](https://clawhub.ai/user/sebayaki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an AI agent run the Mint Club CLI for querying prices and balances, creating tokens, trading through bonding curves, swapping through Uniswap, and transferring ETH or ERC-20 tokens on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to a crypto wallet and operations involving real funds. <br>
Mitigation: Use a dedicated low-balance Base wallet and avoid entering a main private key. <br>
Risk: Trading, swapping, token creation, transfers, and ERC-20 approvals can move assets or create irreversible blockchain transactions. <br>
Mitigation: Require human approval before every trade, swap, transfer, token creation, or ERC-20 approval. <br>
Risk: The skill depends on an external CLI package for wallet and transaction behavior. <br>
Mitigation: Verify the mint.club-cli package and version independently before installation or use. <br>


## Reference(s): <br>
- [Mint Club V2 Docs](https://docs.mint.club) <br>
- [mint.club-cli npm package](https://www.npmjs.com/package/mint.club-cli) <br>
- [Mint Club](https://mint.club) <br>
- [Mint Club Community](https://onchat.sebayaki.com/mintclub) <br>
- [ClawHub Skill Page](https://clawhub.ai/sebayaki/mintclub) <br>
- [Publisher Profile](https://clawhub.ai/user/sebayaki) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may initiate wallet, token creation, trade, swap, transfer, or ERC-20 approval actions against real funds on Base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
