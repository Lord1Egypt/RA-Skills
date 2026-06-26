## Description: <br>
Manage Stellar wallets, send XLM payments, configure networks, and interact with Soroban smart contracts through the Stellar CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sixela33](https://clawhub.ai/user/Sixela33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to perform Stellar CLI workflows such as wallet setup, testnet funding, network configuration, XLM payments, and Soroban smart contract interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and fund wallets, change Stellar networks, and remove keys through Stellar CLI commands with limited confirmation. <br>
Mitigation: Review commands before execution and require explicit user confirmation before wallet creation, funding, network changes, mainnet use, secret-key access, or key removal. <br>
Risk: The skill depends on installing or invoking the Stellar CLI from external distribution channels. <br>
Mitigation: Inspect the Stellar CLI install source or package metadata and verify the installed binary before use. <br>
Risk: Using mainnet can affect real funds. <br>
Mitigation: Keep workflows on testnet by default and proceed on mainnet only after the user explicitly confirms the network and transaction details. <br>


## Reference(s): <br>
- [Stellar CLI documentation](https://developers.stellar.org/docs/tools/developer-tools/cli) <br>
- [Stellar CLI install script](https://github.com/stellar/stellar-cli/raw/main/install.sh) <br>
- [Stellar CLI crate](https://crates.io/crates/stellar-cli) <br>
- [Stellar CLI releases](https://github.com/stellar/stellar-cli/releases/latest) <br>
- [ClawHub skill page](https://clawhub.ai/Sixela33/open-stellar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command blocks and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Stellar CLI binary and may operate on local Stellar key material and configured networks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
