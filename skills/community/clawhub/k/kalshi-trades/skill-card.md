## Description: <br>
Read-only Kalshi OpenAPI scouting skill for market discovery, liquidity checks, and market validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to inspect Kalshi exchange status, discover markets, events, and series, and validate market tickers, trades, and order books before any separate paper-trading workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes external Kalshi API requests and can be configured to use a different base URL. <br>
Mitigation: Review the requested command and KALSHI_BASE_URL value before execution, especially in environments with network restrictions. <br>
Risk: Market, trade, and order book data can be incomplete, delayed, or misread when used for scouting decisions. <br>
Mitigation: Validate important market details against Kalshi's official interface or documentation before relying on the output. <br>
Risk: The skill is read-only, but its output may be paired with a separate paper-trading or execution workflow. <br>
Mitigation: Keep execution in a separate reviewed skill and confirm that no order placement, amendment, or cancellation command is introduced here. <br>


## Reference(s): <br>
- [Kalshi Documentation](https://docs.kalshi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/BRS999/kalshi-trades) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples; CLI commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; supports optional KALSHI_BASE_URL override; read-only OpenAPI requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
