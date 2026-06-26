## Description: <br>
Read-only Kalshi API skill for market discovery, liquidity checks, and market validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query read-only Kalshi market data, inspect liquidity, and validate market candidates before separate analysis or paper-trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom KALSHI_BASE_URL values send requested tickers and filters to the configured endpoint. <br>
Mitigation: Leave KALSHI_BASE_URL unset or set it only to a trusted Kalshi-compatible endpoint. <br>
Risk: A separate paper-trading or execution skill may introduce different trading or account risks. <br>
Mitigation: Review any separate paper-trading or execution skill independently before using it with this read-only market-data skill. <br>


## Reference(s): <br>
- [Kalshi API Documentation](https://docs.kalshi.com) <br>
- [Kalshi Trade API Base Endpoint](https://api.elections.kalshi.com/trade-api/v2) <br>
- [ClawHub Release Page](https://clawhub.ai/BRS999/kalshi-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market data helper; requires Node.js.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
