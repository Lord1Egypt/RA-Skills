## Description: <br>
Enables trustless atomic swaps and escrow for inscriptions and NFTs on EVM chains using Hash Time Locked Contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web4agent](https://clawhub.ai/user/web4agent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use this skill to generate HTLC trade secrets, lock ETH, reveal preimages, and inspect trade status for peer-to-peer inscription, NFT, escrow, or digital asset swaps on EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real ETH when provided a private key. <br>
Mitigation: Use only a dedicated low-value wallet with funds the operator can afford to lose, and require explicit approval for every transaction. <br>
Risk: An HTLC preimage can release funds if shared at the wrong step. <br>
Mitigation: Protect preimages until the correct reveal step has been independently confirmed. <br>
Risk: Autonomous live trades can execute against the wrong contract, chain, or counterparty. <br>
Mitigation: Do not allow autonomous live trades; verify the contract, chain, amount, and counterparty independently before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/web4agent/htlc) <br>
- [README.md](README.md) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>
- [Irys gateway](https://gateway.irys.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wallet, RPC, contract, seller, hash, timeout, amount, lock hash, or preimage inputs depending on the command.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
