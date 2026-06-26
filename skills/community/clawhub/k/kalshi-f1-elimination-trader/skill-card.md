## Description: <br>
Trades F1 Drivers Championship markets on Kalshi by identifying mathematically eliminated drivers still priced above zero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to scan Kalshi F1 Drivers Championship markets for mathematically eliminated drivers, report opportunities, and optionally place live NO trades when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real trades using high-value trading and wallet credentials. <br>
Mitigation: Start in dry-run mode, enable live trading only with an explicit --live run, and use a dedicated low-balance Solana wallet. <br>
Risk: The trading signal relies on static hard-coded F1 standings that may be stale. <br>
Mitigation: Review and update the standings before any live run, or replace the template signal with a trusted live F1 data source. <br>
Risk: The skill depends on SIMMER_API_KEY, SOLANA_PRIVATE_KEY, and the simmer-sdk package for trading access. <br>
Mitigation: Verify the API key, wallet scope, and dependency source before enabling live or automaton execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-f1-elimination-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Console text and JSON status summaries, with Markdown setup guidance and Python code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode reports opportunities without placing trades; live mode can execute trades through the configured Simmer/Kalshi connection.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
