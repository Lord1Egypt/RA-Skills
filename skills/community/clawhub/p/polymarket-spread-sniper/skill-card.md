## Description: <br>
Snipe mispriced Polymarket markets by comparing AMM price vs live CLOB orderbook midpoint, buying the underpriced side when the configured spread threshold is met and exiting via take-profit or time-stop rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prysm96](https://clawhub.ai/user/prysm96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-bot operators use this skill to run or inspect an automated Polymarket spread strategy that scans markets, manages entries and exits, and reports position and P&L state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute live automated trades when run with --live or scheduled as a job. <br>
Mitigation: Use dry runs first, enable live mode only intentionally, and monitor position, daily spend, and P&L logs during operation. <br>
Risk: Bundled risk limits may allow more exposure than a user expects, including a very high daily spend cap in config.json. <br>
Mitigation: Lower max position, max trades per run, and daily spend limits in config.json or environment variables before live use. <br>
Risk: SIMMER_API_KEY grants trading-related authority and may be loaded from the workspace environment. <br>
Mitigation: Use a restricted key with only the funds and permissions intended for this bot, and avoid broad shared .env files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/prysm96/polymarket-spread-sniper) <br>
- [Simmer API endpoint used by the skill](https://api.simmer.markets/api/sdk/positions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, plus command-line text, JSON status output, and local JSON/log files from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and writes local position, daily spend, and P&L state when executed.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
