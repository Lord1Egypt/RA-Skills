## Description: <br>
Trades Polymarket prediction markets on FDA drug approvals, biotech IPOs, clinical trial outcomes, pharma M&A, and precision medicine milestones using biotech event signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run a paper-first Polymarket trading workflow for biotech and FDA event markets. It discovers candidate markets, applies configurable trading thresholds and safeguards, and can place live trades only when explicitly run with live credentials and the --live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades when run with --live and a live-capable SIMMER_API_KEY. <br>
Mitigation: Use paper mode first, keep live-capable credentials out of default environments, and require explicit approval before any --live run. <br>
Risk: Advertised safeguards may not fully match the code, including volume, days-to-resolution, position limits, and manual approval controls. <br>
Mitigation: Verify or add those safeguards before live use, and set conservative tunables for trade size, market volume, spread, resolution window, and open positions. <br>
Risk: The skill requires a sensitive trading API credential. <br>
Mitigation: Store SIMMER_API_KEY only in a secret manager or protected runtime environment, review dependency behavior, and revoke or rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Polymarket Biotech Trader on ClawHub](https://clawhub.ai/diagnostikon/polymarket-biotech-trader) <br>
- [FDA Drug Review Process](https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review) <br>
- [ClinicalTrials.gov API](https://clinicaltrials.gov/api/) <br>
- [SEC EDGAR Search](https://efts.sec.gov/LATEST/search-index?q=%22biotech%22&dateRange=custom) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance plus plain-text execution logs and trading API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; live trading requires the explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
