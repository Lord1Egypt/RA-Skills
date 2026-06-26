## Description: <br>
Automates Polymarket BTC, ETH, and SOL fast-market trading using CEX price momentum signals through the Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redrepz](https://clawhub.ai/user/redrepz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to evaluate or run short-window Polymarket crypto fast-market strategies, configure trading thresholds and sizing, and optionally place live trades after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades and uses wallet signing credentials. <br>
Mitigation: Start in dry-run mode, use a dedicated low-balance wallet, verify the Simmer SDK and publisher, and set strict daily and per-trade limits before enabling live trading. <br>
Risk: Unattended cron or heartbeat live mode can continue trading without timely human review. <br>
Mitigation: Avoid scheduled live mode unless it is actively monitored and can be disabled quickly. <br>
Risk: Fast markets can be sensitive to fees, liquidity, and short-window signal quality. <br>
Mitigation: Review the strategy settings, fee assumptions, and market conditions before relying on trade recommendations or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redrepz/polymarketbot) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Default configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live mode can place Polymarket trades when configured with credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
