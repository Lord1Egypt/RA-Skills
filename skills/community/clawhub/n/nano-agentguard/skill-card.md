## Description: <br>
Agent Identity & Permission Guardian - Trust middleware for credential management, permission scopes, human approval workflows, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sendwealth](https://clawhub.ai/user/sendwealth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use AgentGuard to store agent credentials, define permission scopes, require approval for dangerous operations, and audit agent activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential handling has high-impact safety gaps, including risky secret output and a default master-password concern identified by the authoritative security evidence. <br>
Mitigation: Review before installing, use test credentials or a contained environment, remove default credential behavior, and make secret output opt-in before production use. <br>
Risk: Shell command construction was flagged as a safety gap by the authoritative security evidence. <br>
Mitigation: Replace shell command construction with argument-based execution and review command paths before enabling the tool in agent workflows. <br>
Risk: External approval notifications may expose sensitive operation details or reach unintended Feishu destinations. <br>
Mitigation: Redact notification payloads, restrict approval destinations, and avoid dangerous auto-approve unless the agents and operations are fully controlled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sendwealth/nano-agentguard) <br>
- [Publisher profile](https://clawhub.ai/user/sendwealth) <br>
- [AgentGuard README](README.md) <br>
- [Feishu Integration](docs/FEISHU-INTEGRATION.md) <br>
- [Credit Score System](docs/CREDIT-SCORE.md) <br>
- [1Password Comparison](docs/1PASSWORD-COMPARISON.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JavaScript examples, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce approval instructions, credential-management commands, audit-report guidance, and configuration snippets.] <br>

## Skill Version(s): <br>
0.4.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
