## Description: <br>
Pair NO-advance with YES-winner legs for the same 2026 World Cup team to trade cross-market mispricing. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[alyna123t](https://clawhub.ai/user/alyna123t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to scan 2026 World Cup prediction markets, compare paired advancement and outright-winner prices, and optionally execute small paired trades after reviewing the risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can place real-money prediction-market trades using SIMMER_API_KEY. <br>
Mitigation: Start with dry-run or sim mode, use a dedicated limited-funded account or key, and enable --live only when intentional trading is desired. <br>
Risk: The included account-status script can read broader Simmer account balance and position data. <br>
Mitigation: Review the helper script before use and provide only the minimum credential scope needed for the intended account. <br>
Risk: Disabling safeguards can bypass spread, slippage, and context checks. <br>
Mitigation: Keep safeguards enabled unless the operator understands which checks are being bypassed and accepts the trading risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alyna123t/polymarket-world-cup-delta-pairs) <br>
- [Publisher profile](https://clawhub.ai/user/alyna123t) <br>
- [Strategy source](https://x.com/zETHerka/status/2061162222156460540) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Command-line text with JSON-backed configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live mode can place paired market trades when enabled.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
