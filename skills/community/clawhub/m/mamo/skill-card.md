## Description: <br>
Interact with Mamo DeFi yield strategies on Base (Moonwell). Deposit/withdraw USDC, cbBTC, MAMO, or ETH into automated yield strategies. Check APY rates and account status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anajuliabit](https://clawhub.ai/user/anajuliabit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Mamo yield strategies on Base, including creating strategy contracts, depositing or withdrawing supported tokens, checking balances, and reviewing APY data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can use a wallet private key to approve token spending and sign real Base mainnet transactions. <br>
Mitigation: Use a dedicated hot wallet with limited funds, try dry-run mode first, and review create, deposit, and withdraw commands before execution. <br>
Risk: Status and APY features may share a wallet address with Mamo or Moonwell services. <br>
Mitigation: Use the skill only when that address-sharing behavior is acceptable for the wallet involved. <br>
Risk: Private keys exposed through committed files, shell history, or shared environments can lead to loss of funds. <br>
Mitigation: Keep MAMO_WALLET_KEY out of committed files and use a scoped environment for wallet-signing commands. <br>


## Reference(s): <br>
- [Mamo CLI README](README.md) <br>
- [Mamo Contract Addresses and ABIs](references/contracts.md) <br>
- [Mamo API Reference](references/mamo-api.md) <br>
- [Mamo](https://mamo.xyz) <br>
- [Moonwell](https://moonwell.fi) <br>
- [Mamo Docs](https://docs.mamo.xyz) <br>
- [Mamo Contracts](https://github.com/moonwell-fi/mamo-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON] <br>
**Output Format:** [CLI text output, command guidance, and JSON when the --json option is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a MAMO_WALLET_KEY for wallet-signing operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
