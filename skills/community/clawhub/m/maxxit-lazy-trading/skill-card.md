## Description: <br>
Execute perpetual trades on Ostium, Aster, and Avantis via Maxxit's Lazy Trading API, and trade Indian stocks through Zerodha Kite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhi152003](https://clawhub.ai/user/abhi152003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agent operators use this skill to research markets, inspect balances and positions, open or close trades, manage take-profit and stop-loss settings, copy-trade, and run bundled strategy scripts through Maxxit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically place or modify live trades with limited safeguards. <br>
Mitigation: Install only when the agent is intended to have live trading authority; verify MAXXIT_API_URL, keep API keys secret and scoped, and use dry-run or explicit approval before risking funds. <br>
Risk: Strategy scripts can execute leveraged trades based on market data and configured venue settings. <br>
Mitigation: Set strict collateral, leverage, venue, take-profit, and stop-loss limits before use, and review proposed strategy behavior before running against real funds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abhi152003/maxxit-lazy-trading) <br>
- [Publisher Profile](https://clawhub.ai/user/abhi152003) <br>
- [Maxxit App](https://maxxit.ai) <br>
- [Lazy Trading Setup](https://maxxit.ai/lazy-trading) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, Python strategy invocations, endpoint payloads, and concise trading guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXXIT_API_KEY and MAXXIT_API_URL; bundled Python scripts may create local state and log files in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.2.20 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
