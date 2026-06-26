## Description: <br>
Trades the highest-edge active AION Polymarket market matching a query using a user-supplied fair probability, AION context safeguards, and Kelly-style sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to evaluate active Polymarket markets with a user-supplied fair probability signal, apply AION context safeguards and Kelly-style sizing, and run dry-run or explicitly enabled live order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring financial automation can affect a Polymarket account, including auto-redeeming resolved positions even when live trading is disabled. <br>
Mitigation: Start in dry-run with a controlled account, use limited balances and scoped credentials, and require separate explicit opt-in for auto-redeem and live trading before scheduling recurring runs. <br>
Risk: Live trading requires wallet-related inputs and signed order data. <br>
Mitigation: Avoid private keys where possible, keep wallet credentials out of shared environments, and use signed order JSON only for intentional live executions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fivegive249-ship-it/polymarket-edge-trader) <br>
- [AION agent portal](https://pm-t1.bxingupdate.com/agents) <br>
- [AION API base URL](https://pm-t1.bxingupdate.com/bvapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with command examples and Python script output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AION_API_KEY; live trading requires explicit --live mode plus wallet address and signed order JSON.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
