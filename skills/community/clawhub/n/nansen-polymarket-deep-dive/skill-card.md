## Description: <br>
Deep dive on a Polymarket market: OHLCV, orderbook, top holders, positions, trades, and PnL leaderboard for a specific prediction market. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to investigate a specific Polymarket prediction market by retrieving market history, orderbook depth, holder positions, trades, and PnL data through the Nansen CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use of the Nansen CLI requires trusting the installed nansen-cli package and protecting a Nansen API key. <br>
Mitigation: Use a dedicated or least-privileged NANSEN_API_KEY, avoid exposing it in logs, and keep usage focused on the documented nansen research pm commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-polymarket-deep-dive) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and tabular CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; commands are scoped to nansen research pm market analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
