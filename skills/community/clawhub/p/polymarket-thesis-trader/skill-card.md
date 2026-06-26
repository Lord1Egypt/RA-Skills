## Description: <br>
Scan Polymarket markets for a configurable thesis, compare your probability to the market price, and trade only when the edge clears a safety threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scan Polymarket markets for a configured thesis, compare market prices with a supplied fair probability, and dry-run or execute trades when configured edge and safety checks pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades on a 15-minute schedule using an API key and live-mode environment setting. <br>
Mitigation: Keep RUN_LIVE unset unless real trades are intended, monitor scheduled runs, and review parameters before enabling live operation. <br>
Risk: Trading losses or repeated unintended trades may not be reversible. <br>
Mitigation: Use a limited-funded account or restricted key when available, and set conservative TRADE_AMOUNT_USD, MIN_EDGE, MIN_ENTRY_PRICE, and MAX_ENTRY_PRICE values. <br>
Risk: The skill requires a sensitive AION_API_KEY for market reads and trade execution. <br>
Mitigation: Store the key in environment configuration, avoid logging or committing it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fivegive249-ship-it/polymarket-thesis-trader) <br>
- [Publisher profile](https://clawhub.ai/user/fivegive249-ship-it) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal summary text with CLI and environment configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit live AION SDK trade requests when explicitly run with live trading enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
