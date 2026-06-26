## Description: <br>
DEPRECATED. Use jun-invest-option-master-agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this deprecated release as a pointer away from jun-invest-option-master and toward the replacement jun-invest-option-master-agent. The bundled workspace evidence describes an investment research agent that prepares approval packets for human review and does not automatically place trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is deprecated but still includes active installation, update, registration, git hook, scheduled publishing, and account-linking workflows. <br>
Mitigation: Review scripts before installation and avoid auto-install unless local workspace changes, agent registration, scheduled publishing, and account linking are intended. <br>
Risk: Linked messaging, broker, or market-data accounts may expose local data or credentials to the workspace. <br>
Mitigation: Do not link WhatsApp, Telegram, broker, or market-data accounts unless the required access and credential handling are understood. <br>
Risk: Investment approval packets can be incomplete, stale, or wrong even though the artifact states that it does not automatically place trades. <br>
Mitigation: Require human review and approval before any trade and validate data freshness, cash coverage, risk limits, and order details independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gm4leejun-stack/jun-invest-option-master) <br>
- [README](README.md) <br>
- [Investment agent workspace README](agent/invest_agent/README.md) <br>
- [Investment agent charter](docs/INVESTMENT_AGENT.md) <br>
- [Futu OpenAPI documentation](https://openapi.futunn.com/futu-api-doc/intro/intro.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown approval packets, JSON validation reports, configuration files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deprecated release; review security guidance before installing or linking accounts.] <br>

## Skill Version(s): <br>
0.99.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
