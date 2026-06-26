## Description: <br>
Automated Kalshi prediction market trading bot that scans markets, researches opportunities, places trades under EV IRR and half-Kelly rules, monitors positions, and reports summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobthemom987](https://clawhub.ai/user/bobthemom987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and developers use this skill to set up an automated agent that scans Kalshi markets, evaluates candidate trades, interacts with the Kalshi API, and reports account and position summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables unattended real-money trading with stored Kalshi credentials and limited explicit safety controls. <br>
Mitigation: Install only when unattended access to a real Kalshi account is intended; use a small limited balance, review and edit the cron prompt before enabling it, and avoid scheduled live trading unless automated-loss risk is accepted. <br>
Risk: The bot stores API key material on disk and uses it to sign Kalshi API requests. <br>
Mitigation: Use tightly permissioned key files or a safer secret store, rotate or revoke the API key when finished, and restrict access to the account and host running the bot. <br>


## Reference(s): <br>
- [Kalshi Trader release page](https://clawhub.ai/bobthemom987/kalshi-trader) <br>
- [Kalshi API Reference](references/api.md) <br>
- [Cron Prompt for 15-Minute Scan](references/cron-prompt.md) <br>
- [Trade Research Workflow](references/trade-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python code, configuration steps, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance, scheduled scan prompts, trading rules, API examples, and account summary output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
