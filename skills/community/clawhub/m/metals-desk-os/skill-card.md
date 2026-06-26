## Description: <br>
Institutional Desk-Level Fully Automated Trading OS for XAU/USD and XAG/USD that runs continuous analysis, risk management, performance tracking, and optional MT5 execution inside OpenClaw's trader agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cfilipemt](https://clawhub.ai/user/cfilipemt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and trading developers use this skill to analyze XAU/USD and XAG/USD market conditions, generate trade plans, monitor risk, and optionally route execution through MT5. Start with demo or paper credentials and Advisory mode before any live trading use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated or semi-automated operation can affect a real broker account. <br>
Mitigation: Begin with demo or paper credentials and Advisory mode, and do not enable Semi-Automated or Fully-Automated modes until live execution approvals and safeguards are fixed. <br>
Risk: Unauthenticated WebSocket mode control can change system behavior. <br>
Mitigation: Restrict the WebSocket service to trusted local access or remove command handling before deployment. <br>
Risk: Trading credentials and alert tokens are configured through environment variables. <br>
Mitigation: Protect the .env file, limit credential scope, and avoid sharing configured release copies. <br>
Risk: Known buy/sell order and simulated-price fallback issues can undermine live execution reliability. <br>
Mitigation: Fix those issues and validate in paper trading before allowing broker-connected execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cfilipemt/metals-desk-os) <br>
- [Publisher profile](https://clawhub.ai/user/cfilipemt) <br>
- [MetaAPI](https://metaapi.cloud) <br>
- [Telegram Bot API](https://api.telegram.org) <br>
- [WhatsApp Business Platform](https://graph.facebook.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text instructions, JSON dashboard payloads, event logs, alerts, and broker action requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run continuously as an event-driven trading workflow with Advisory, Semi-Automated, Fully-Automated, and Risk-Off modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
