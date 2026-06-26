## Description: <br>
Send and receive KAS cryptocurrency, check balances, send payments, and generate wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manyfestation](https://clawhub.ai/user/Manyfestation) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to manage a Kaspa wallet from the command line, including balance checks, fee estimates, wallet generation, payment URI creation, and KAS transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wallet can send KAS from configured credentials without an interactive confirmation step. <br>
Mitigation: Require separate human approval before any send or max transaction, especially on mainnet. <br>
Risk: Wallet secrets are supplied through KASPA_PRIVATE_KEY or KASPA_MNEMONIC environment variables. <br>
Mitigation: Use a small dedicated wallet or testnet first, avoid primary seed phrases, and keep these environment variables out of shared shells and logs. <br>
Risk: The installer downloads and uses the kaspa Python package. <br>
Mitigation: Review the installed kaspa package and dependency source before allowing wallet operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Manyfestation/kaspa-wallet) <br>
- [Kaspa mainnet transaction explorer](https://explorer.kaspa.org/txs/{txid}) <br>
- [Kaspa testnet transaction explorer](https://explorer-tn10.kaspa.org/txs/{txid}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return structured JSON and use environment variables for wallet credentials, network selection, RPC endpoint, and timeout configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
