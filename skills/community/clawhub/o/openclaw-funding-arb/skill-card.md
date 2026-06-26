## Description: <br>
Runs and maintains a MEXC stock-contract funding-rate arbitrage bot with millisecond timing, funding-rate threshold filters, stock allowlists, U.S. regular-session controls, and persistent recovery of open-position state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshengyyy](https://clawhub.ai/user/linshengyyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run, tune, troubleshoot, or modify a MEXC stock-contract funding-rate arbitrage workflow that opens and closes leveraged positions around funding settlement windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live leveraged MEXC trades using sensitive API credentials. <br>
Mitigation: Use a dedicated least-privilege MEXC API key with withdrawals disabled, reduce leverage from the default, and run only on an account balance you are prepared to put at risk. <br>
Risk: Default sizing and missing caps can allow larger exposure than intended. <br>
Mitigation: Set explicit MAX_NOTIONAL_USDT or MAX_OPEN_VOL limits before running and monitor order execution. <br>
Risk: Open-position recovery depends on a local state file. <br>
Mitigation: Choose a dedicated STATE_FILE path, protect it from accidental deletion or disclosure, and verify recovery behavior before unattended use. <br>


## Reference(s): <br>
- [MEXC Contract API](https://contract.mexc.com) <br>
- [ClawHub skill page](https://clawhub.ai/linshengyyy/openclaw-funding-arb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands, environment-variable configuration, and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational tuning advice for API credentials, timing windows, order sizing, state recovery, and risk controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
