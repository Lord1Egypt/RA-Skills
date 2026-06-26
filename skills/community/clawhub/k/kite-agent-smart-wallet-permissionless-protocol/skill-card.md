## Description: <br>
Create and manage modular, permissioned smart wallets for AI agents with session keys and spending limits on the Kite AI network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaovand](https://clawhub.ai/user/nihaovand) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building blockchain-enabled agents use this skill to understand wallet setup on Kite AI, including session keys, spending limits, deployed contract addresses, and network endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet actions and session-key examples can affect blockchain assets if used with real funds or broad permissions. <br>
Mitigation: Use testnet first, decode each transaction before signing, keep session-key spending limits narrow, and revoke session keys when they are no longer needed. <br>
Risk: Incorrect contract addresses or RPC endpoints can route users to unintended network interactions. <br>
Mitigation: Verify contract addresses and RPC endpoints against official Kite sources before executing wallet operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nihaovand/kite-agent-smart-wallet-permissionless-protocol) <br>
- [Kite AI Docs](https://docs.gokite.ai) <br>
- [Biconomy Nexus](https://docs.biconomy.io/new/learn-about-biconomy/nexus) <br>
- [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) <br>
- [ERC-7579](https://eips.ethereum.org/EIPS/eip-7579) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript examples and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes contract addresses, chain IDs, RPC endpoints, explorer links, and wallet interaction examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
