## Description: <br>
Query and trade perpetual futures through LiberFi's unified perpetuals API for Hyperliquid-backed market data, account reads, and signed order, cancel, and deposit flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect perpetual futures markets, read authenticated LiberFi account data, prepare signed trading actions, and fund Hyperliquid perpetual accounts from Solana through LiberFi CLI flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent account access can expose private trading data or sensitive wallet-linked account reads. <br>
Mitigation: Verify the LiberFi account and wallet before account reads, and know how to revoke the agent login. <br>
Risk: Deposits, order submissions, and cancellations can move funds or alter live trading positions. <br>
Mitigation: Require explicit confirmation of the amount, recipient, market, side, size, fees, and signed action before any submit or deposit command. <br>
Risk: The skill may install and rely on a global LiberFi CLI. <br>
Mitigation: Install only if the publisher and CLI are trusted, or verify and install the CLI manually before using the skill. <br>


## Reference(s): <br>
- [Perp Deposit Flow](reference/deposit-flow.md) <br>
- [LiberFi Homepage](https://liberfi.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/bombmod/liberfi-perpetuals) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-oriented result handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before order submission, cancellation submission, or deposit placement.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact metadata.version is 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
