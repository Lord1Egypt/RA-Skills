## Description: <br>
Helps agents scan and rank Pendle Principal Token markets, monitor fixed-yield positions, and prepare managed-wallet or manual execution plans with explicit confirmation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moshu](https://clawhub.ai/user/moshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to research Pendle PT fixed-yield opportunities, compare stable-ish markets, monitor maturities, and prepare deposit, redeem, withdraw, or rollover plans. It is intended for planning and managed-wallet or manual execution workflows, not bundled private-key signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pendle deposit, redeem, withdraw, or rollover planning can lead to real onchain financial actions. <br>
Mitigation: Require explicit user confirmation after showing the wallet path, market, amount, maturity, slippage or price impact, gas, and notable asset risks. <br>
Risk: Private keys or seed phrases could be mishandled if a host tries to add raw local signing around the skill. <br>
Mitigation: Use managed wallets with policy controls or manual user-executed wallet flows, and do not provide private keys or seed phrases to the skill. <br>
Risk: Quotes, liquidity, slippage, maturity dates, and underlying-asset risks can change before execution. <br>
Mitigation: Re-check quote freshness, slippage thresholds, gas cost, market liquidity, maturity, and underlying asset quality immediately before any confirmation. <br>
Risk: PT fixed yield depends on holding to maturity, while early exits may realize less than maturity value. <br>
Mitigation: Clearly distinguish hold-to-maturity expectations from early-exit estimates and warn when an action is a withdrawal or rollover before maturity. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/moshu/pendle-pt-yield-strategy) <br>
- [Chain Addresses](references/chain-addresses.md) <br>
- [Eligible Underlyings for PT Yield Strategy](references/eligible-underlyings.md) <br>
- [Pendle PT Ranking Framework](references/ranking-framework.md) <br>
- [Manual Contango PT Comparison Framework](references/manual-contango-comparison.md) <br>
- [Pendle API Core](https://api-v2.pendle.finance/core) <br>
- [Pendle Active Markets Endpoint](https://api-v2.pendle.finance/core/v1/{chainId}/markets/active) <br>
- [Pendle Convert Quote Endpoint](https://api-v2.pendle.finance/core/v2/sdk/{chainId}/convert) <br>
- [Pendle Convert v3 Endpoint](https://api-v2.pendle.finance/core/v3/sdk/{chainId}/convert) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON market and position files, shell command suggestions, and execution-planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces research and planning artifacts for Pendle PT workflows; runtime transaction submission is expected to occur through a managed wallet backend or a user-controlled manual wallet flow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
