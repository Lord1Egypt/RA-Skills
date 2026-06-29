## Description: <br>
Copy the top World Cup traders on Polymarket using a daily Simmer-curated leader set, with dry-run and sim-first defaults before optional live trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to review or run a World Cup Polymarket copy-trading workflow that mirrors a server-curated set of leaders. It is intended to be validated in dry-run or sim mode before any live Polymarket execution with real USDC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket orders, and automated trading losses may be irreversible. <br>
Mitigation: Keep the default dry-run and sim venue until planned trades have been reviewed; use --venue polymarket --live only when real USDC execution is intended. <br>
Risk: Copied leader positions can lose money, and copyability screening does not remove market, slippage, or thin-book risk. <br>
Mitigation: Use conservative WC_COPYTRADER_MAX_USD, WC_COPYTRADER_MAX_TRADES, and WC_COPYTRADER_MAX_SLIPPAGE values before enabling live trading. <br>
Risk: The skill requires sensitive credentials and may use a wallet private key for live external-wallet trading. <br>
Mitigation: Provide credentials through environment variables, protect SIMMER_API_KEY and WALLET_PRIVATE_KEY, and only set WALLET_PRIVATE_KEY when live external-wallet Polymarket execution is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-worldcup-copytrader) <br>
- [Disclaimer](artifact/DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text output with trade plans, leader and position summaries, configuration details, and managed-run JSON status when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live execution requires explicit --live and can target sim or Polymarket based on configuration.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
