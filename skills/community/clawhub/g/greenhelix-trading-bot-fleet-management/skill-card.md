## Description: <br>
Guides agents through building a GreenHelix fleet management layer for 10 or more trading bots with per-bot identity isolation, permission scoping, health monitoring, coordinated deployments, SLA tracking, and cost allocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operations teams use this skill to design a unified control plane for multi-bot trading fleets, including identity isolation, scoped permissions, monitoring, deployments, SLA tracking, and cost attribution. The skill is a guide with Python and curl examples rather than an executable integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples concern trading bots and funds, and the server security verdict is suspicious due to under-specified high-impact safety and credential details. <br>
Mitigation: Audit the guide and examples before adapting them for real bots or capital, and start with sandbox or least-privilege credentials. <br>
Risk: The skill references sensitive credentials including AGENT_SIGNING_KEY and GreenHelix API keys. <br>
Mitigation: Store keys in a managed secret store, scope permissions per bot, rotate keys on a tested schedule, and avoid shared exchange or signing credentials. <br>
Risk: Documented SLA escalation and automatic pause behavior may be mistaken for platform enforcement. <br>
Mitigation: Implement and test pause, failover, and escalation paths in the user's own control plane before relying on them operationally. <br>
Risk: The release evidence and skill frontmatter disagree on the license identifier. <br>
Mitigation: Confirm whether MIT-0 or MIT is authoritative before publishing or redistributing the card. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/mirni/greenhelix-trading-bot-fleet-management) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API reference](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python examples, curl commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference AGENT_SIGNING_KEY and GreenHelix API credentials supplied by the user.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
