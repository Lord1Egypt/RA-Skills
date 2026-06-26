## Description: <br>
Cross-rail spend tracking for AI agents across Visa IC, Mastercard Agent Pay, Stripe ACP, x402, and ACH in one dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an AI agent report financial transactions to PayRail402 for spend tracking, budget enforcement, anomaly detection, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends agent transaction metadata to PayRail402 for spend tracking. <br>
Mitigation: Install only when PayRail402 should receive this data, and avoid including sensitive account or customer details in transaction descriptions unless needed. <br>
Risk: API keys and webhook tokens authorize transaction tracking and status operations. <br>
Mitigation: Keep credentials private, use the least-privileged authentication method that fits the deployment, and keep the service URL on the official HTTPS endpoint. <br>


## Reference(s): <br>
- [PayRail402 homepage](https://payrail402.com) <br>
- [PayRail402 API documentation](https://payrail402.com/llms-full.txt) <br>
- [PayRail402 agent discovery card](https://payrail402.com/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON tool responses with success, status, or error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PayRail402 credentials for authenticated tracking or status checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
