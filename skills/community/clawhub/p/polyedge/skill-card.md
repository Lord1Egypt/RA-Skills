## Description: <br>
Detect mispriced correlations between Polymarket prediction markets. Cross-market arbitrage finder for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sbaker5](https://clawhub.ai/user/sbaker5) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use PolyEdge to compare two Polymarket markets, estimate whether their prices imply a correlation mismatch, and return a signal such as hold, buy yes, buy no, or skip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted or deployed API mode can make outbound calls to Polymarket, Base RPC providers, BaseScan, and api.nshrt.com. <br>
Mitigation: Use the local analyzer when only market comparison is needed, and review network destinations before enabling hosted or deployed API mode. <br>
Risk: Paid API usage can spend $0.05 USDC per request on Base. <br>
Mitigation: Require explicit spend limits and human review before allowing an agent to make paid API calls. <br>
Risk: Payment and dashboard features can expose public wallet or payment activity if deployed without appropriate access controls. <br>
Mitigation: Confirm the wallet visibility is acceptable and restrict dashboard exposure when deploying the service. <br>
Risk: Correlation signals may be incorrect or incomplete and should not be treated as automated trading advice. <br>
Mitigation: Require human review and explicit decision limits before any trading or market action is taken. <br>


## Reference(s): <br>
- [PolyEdge on ClawHub](https://clawhub.ai/sbaker5/polyedge) <br>
- [Publisher profile](https://clawhub.ai/user/sbaker5) <br>
- [Hosted correlation API](https://api.nshrt.com/api/v1/correlation?a=<slug>&b=<slug>) <br>
- [PolyEdge dashboard](https://api.nshrt.com/dashboard) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON analysis results with optional Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return market details, correlation estimates, mispricing values, confidence, and action signals.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
