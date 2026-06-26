## Description: <br>
Access HL Privateer, an agentic Hyperliquid discretionary trading desk for live positions, AI analysis, copy-trade signals, and risk state through x402 pay-per-call endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ADWilkinson](https://clawhub.ai/user/ADWilkinson) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
External agents and developers use this skill to query HL Privateer trading positions, analysis, copy-trade signals, risk state, and WebSocket events for monitoring, signal integration, or copy-trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a third-party paid trading-signal service and may lead agents to query or copy trading activity. <br>
Mitigation: Install it only when you intentionally want access to this service, and require explicit approval before copying trades. <br>
Risk: Paid x402 flows require wallet spending authorization. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit approval before signing payment payloads. <br>
Risk: Operator JWTs or login secrets can allow control of trading-desk commands. <br>
Mitigation: Do not provide operator JWTs or login secrets unless you intentionally want the agent to control the trading desk. <br>
Risk: Private keys or wallet secrets could be exposed if pasted into prompts or source files. <br>
Mitigation: Never paste a real private key into prompts or source files; use a wallet client or secure signing flow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ADWilkinson/hl-privateer-fund) <br>
- [HL Privateer website](https://hlprivateer.xyz) <br>
- [Skill package](https://hlprivateer.xyz/skills/hl-privateer.md) <br>
- [API reference](https://hlprivateer.xyz/skills/api.md) <br>
- [x402 payment guide](https://hlprivateer.xyz/skills/x402.md) <br>
- [OpenAgents discovery](https://hlprivateer.xyz/skills/agents.json) <br>
- [Agent quick start](https://hlprivateer.xyz/skills/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with REST and WebSocket requests, JSON payloads, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to api.hlprivateer.xyz and x402 payment signing for paid agent endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata declares 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
