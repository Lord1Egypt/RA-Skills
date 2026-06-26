## Description: <br>
AI agent for automated prediction market trading on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArubikU](https://clawhub.ai/user/ArubikU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to analyze Polymarket prediction markets, identify arbitrage opportunities, and prepare or execute automated trades under stated portfolio limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-level credentials and private keys may authorize irreversible transactions. <br>
Mitigation: Use only a dedicated low-balance wallet and avoid providing a primary wallet private key. <br>
Risk: Live automated trade authority can cause financial loss if analysis, limits, or execution are wrong. <br>
Mitigation: Require manual confirmation or dry-run mode before live trades, and enforce the stated 5% per-trade limit, 20% stop-loss, and daily reporting. <br>
Risk: Implementation provenance is unavailable for this release. <br>
Mitigation: Verify the actual `mia-polymarket` command from a trusted source and review the publisher-supplied code and credential handling before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ArubikU/mia-polymarket-trader) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market analysis, trade command examples, and wallet/API credential setup guidance; live trading should require human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
