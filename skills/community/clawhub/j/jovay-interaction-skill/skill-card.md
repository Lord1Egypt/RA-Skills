## Description: <br>
Skill for interacting with Jovay or Ethereum network using jovay-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jovay-developer](https://clawhub.ai/user/jovay-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blockchain operators use this skill to prepare Jovay CLI commands for wallet setup, balances, transfers, bridge flows, smart contract calls, transaction lookup, and network configuration on Jovay or Ethereum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys or encryption passwords can be exposed if pasted into chat, logs, or shell history. <br>
Mitigation: Use encrypted wallets or secure local secret handling, avoid sharing secrets with the agent, and start with testnet or low-balance wallets. <br>
Risk: Commands using --broadcast can move funds, change allowances, or submit irreversible transactions on Jovay or Ethereum. <br>
Mitigation: Verify the network, recipient, amount, token, spender, contract, gas settings, and proof data before broadcasting; use non-broadcast output or dry-run modes when appropriate. <br>
Risk: The skill depends on the external jovay-cli npm package and the user's local network configuration. <br>
Mitigation: Install only trusted jovay-cli versions and confirm RPC endpoints, chain selection, and package source before use. <br>


## Reference(s): <br>
- [Jovay Network Information](https://docs.jovay.io/developer/network-information) <br>
- [ClawHub Skill Page](https://clawhub.ai/jovay-developer/jovay-interaction-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/jovay-developer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance may include placeholders for addresses, private keys, RPC URLs, gas limits, proofs, and transaction hashes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
