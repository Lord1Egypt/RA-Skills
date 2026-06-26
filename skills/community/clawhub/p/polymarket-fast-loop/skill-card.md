## Description: <br>
Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to discover Polymarket crypto fast markets, evaluate short-term CEX momentum signals, and run dry-run or live order flows through Simmer. It is intended for users who understand automated prediction-market trading, wallet custody, and position-size controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money Polymarket trades when run live. <br>
Mitigation: Start in dry-run mode, use live mode only after reviewing budget, position size, order behavior, and stop conditions. <br>
Risk: Live trading may require sensitive wallet credentials. <br>
Mitigation: Use a managed wallet or a tightly funded dedicated wallet, and do not paste a main-wallet private key into chat or plaintext configuration. <br>
Risk: Fast markets may resolve before scheduled stop-loss or take-profit monitoring can act. <br>
Mitigation: Treat conservative position sizing and daily budgets as primary controls for 5-minute and 15-minute markets. <br>
Risk: Automated loop or cron execution can repeatedly trade before an operator reviews outcomes. <br>
Mitigation: Avoid unattended live loops until budget limits, max position size, and expected skip conditions have been tested in dry-run mode. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/simmer/polymarket-fast-loop) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Risk disclaimer](artifact/DISCLAIMER.md) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>
- [Simmer V2 migration guide](https://docs.simmer.markets/v2-migration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and Python execution output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live trading requires explicit command flags and credentials.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
