## Description: <br>
Near-expiry conviction trading on Polymarket that scans markets in their final minutes, filters for strongly skewed splits, and places bounded trades against the under-priced side. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to scan near-expiry Polymarket markets, apply configurable split, expiry, sizing, and safeguard rules, and run paper-mode or live bounded trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades and on-chain trades cannot be recalled. <br>
Mitigation: Run paper mode first, use --live only deliberately, and keep max bet and max trades limits conservative. <br>
Risk: WALLET_PRIVATE_KEY can authorize trades from the connected wallet. <br>
Mitigation: Avoid providing WALLET_PRIVATE_KEY unless self-custody live trading is required and the operator understands the signing risk. <br>
Risk: The scanner may also redeem existing winning positions before starting a cycle. <br>
Mitigation: Review account-changing behavior before connecting real funds and monitor positions with scripts/status.py. <br>
Risk: Smart sizing and platform-level limits may not match the user's intended exposure. <br>
Mitigation: Verify the effective configured limits, avoid broad smart sizing until tested, and keep platform controls aligned with config values. <br>
Risk: Default strategy parameters are not validated as profitable and fast-resolving markets can outpace monitoring. <br>
Mitigation: Treat defaults as a starting point, test in dry run over time, and size positions conservatively. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-mert-sniper) <br>
- [Strategy attribution thread](https://x.com/mert/status/2020216613279060433) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>
- [Simmer V2 migration guide](https://docs.simmer.markets/v2-migration) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May place live trades when run with --live and valid credentials; defaults to paper mode.] <br>

## Skill Version(s): <br>
1.3.3 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
