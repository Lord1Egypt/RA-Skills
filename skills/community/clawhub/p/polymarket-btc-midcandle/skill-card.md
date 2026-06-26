## Description: <br>
Runs a configurable Python bot that paper-trades or live-trades Polymarket BTC 15-minute markets using mid-candle momentum from Binance price data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjDyll](https://clawhub.ai/user/DjDyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to configure and run a BTC mid-candle Polymarket trading strategy, starting in paper mode and optionally enabling live automated trades after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make unattended real-money trades when live mode and cron are enabled. <br>
Mitigation: Run in paper mode first, review results before enabling live mode, and use a dedicated low-balance, revocable API key. <br>
Risk: Live safeguards can be bypassed with the no-safeguards option. <br>
Mitigation: Avoid disabling safeguards for live funds and review trade behavior before changing risk controls. <br>
Risk: Trade details may be sent to a configured Discord webhook. <br>
Mitigation: Configure a webhook only for trusted endpoints where sharing trade details is acceptable. <br>
Risk: Expected volume confirmation depends on the configured volume gate. <br>
Mitigation: Explicitly set the volume threshold if volume confirmation is required for the trading strategy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DjDyll/polymarket-btc-midcandle) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Runtime configuration](artifact/clawhub.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with CLI commands and optional JSON automaton status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can place live trades when run with live mode; default usage is paper mode.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
