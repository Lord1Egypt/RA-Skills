## Description: <br>
Automates paper or live Polymarket ETH 15-minute market trading using ETH momentum, BTC alignment, volume, timing, and configurable risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjDyll](https://clawhub.ai/user/DjDyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent operators use this skill to configure an automated ETH mid-candle strategy, test it in paper mode, and optionally place live Polymarket orders when configured market signals pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money Polymarket trades on a schedule. <br>
Mitigation: Start in paper mode, keep bet sizes and account exposure small, and monitor behavior before enabling live mode or cron. <br>
Risk: Live-mode safeguards can be disabled with the no-safeguards option. <br>
Mitigation: Avoid disabling safeguards in live mode and keep slippage, flip-flop, and circuit-breaker protections enabled. <br>
Risk: Optional Discord notifications may send trade details to a configured webhook endpoint. <br>
Mitigation: Configure a Discord webhook only when sharing those trade details with that endpoint is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DjDyll/polymarket-eth-midcandle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Terminal text with optional JSON automaton summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper mode; live trading, cron scheduling, smart sizing, and risk settings are user-configurable.] <br>

## Skill Version(s): <br>
1.1.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
