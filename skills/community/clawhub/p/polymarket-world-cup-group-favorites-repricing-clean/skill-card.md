## Description: <br>
Buys pre-tournament World Cup outright favorite positions and optionally exits around the knockout phase to capture group-stage repricing. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[alyna123t](https://clawhub.ai/user/alyna123t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prediction-market operators can use this skill to scan World Cup 2026 outright markets, evaluate repricing edges, run dry-run simulations, inspect positions, and place user-invoked live trades when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global, subject to venue availability and the user's local prediction-market compliance obligations. <br>

## Known Risks and Mitigations: <br>
Risk: Live runs can place prediction-market trades using the user's Simmer API key. <br>
Mitigation: Start with dry-run or sim mode, keep --live disabled until reviewed, and set conservative daily budget, position size, slippage, spread, and trade-count limits. <br>
Risk: The exit workflow can sell matching World Cup outright YES positions around the configured knockout date. <br>
Mitigation: Review manage_exits, current positions, and knockout_start_utc before running live near or after the knockout phase. <br>
Risk: Disabling safeguards can skip context checks intended to avoid resolved markets or severe warning states. <br>
Mitigation: Avoid --no-safeguards unless the operator has reviewed the market context and accepts the additional trading risk. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/alyna123t/polymarket-world-cup-group-favorites-repricing-clean) <br>
- [Strategy source post](https://x.com/airdrops_io/status/2061459289059754392) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and JSON, with configuration values and trade or position summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires SIMMER_API_KEY and an explicit --live or --positions invocation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
