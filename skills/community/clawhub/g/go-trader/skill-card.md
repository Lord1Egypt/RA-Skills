## Description: <br>
Control and monitor the go-trader cryptocurrency trading system with natural language commands for strategies, status, risk, and emergency stops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberleo986](https://clawhub.ai/user/cyberleo986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to control a local go-trader cryptocurrency trading bot, inspect status and logs, manage service health, and trigger emergency stops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect a cryptocurrency trading service that may be connected to live funds. <br>
Mitigation: Install only on hosts you control, keep the bot in paper mode by default, and require explicit approval before live trading or service-control actions. <br>
Risk: Emergency stop, start, restart, and reset-style actions can change trading availability or state. <br>
Mitigation: Use external account limits, exchange permissions without withdrawals, and operational review before enabling these commands for real-money environments. <br>


## Reference(s): <br>
- [Go Trader on ClawHub](https://clawhub.ai/cyberleo986/go-trader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local service-control commands and status-check guidance for a go-trader host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
