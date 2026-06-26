## Description: <br>
Trades Polymarket prediction markets on landmark court cases, antitrust rulings, SEC enforcement actions, EU regulatory decisions, and DOJ investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agent builders use this skill to discover legal and regulatory Polymarket markets, generate paper-trade orders by default, and optionally place live trades when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades and cause financial loss. <br>
Mitigation: Run in paper mode first, keep position limits conservative, and use --live only when accepting real-money loss risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Protect the key, avoid committing it to files or logs, and rotate it if exposure is suspected. <br>
Risk: The skill depends on simmer-sdk for market discovery and trade execution. <br>
Mitigation: Verify the simmer-sdk package source and version before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-legal-regulatory-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Python script execution with console logs and simulated or live trade API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires SIMMER_API_KEY and an explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
