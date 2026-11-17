## Description:

DEPRECATED. Use jun-invest-option-master-agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this deprecated installer only to migrate or synchronize the jun-invest-option-master workspace assets. The packaged workspace supports investment research and option-strategy approval packets, with all trading actions requiring human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated installer includes update, install, and agent-registration workflows that can change local agent state.

Mitigation: Require explicit human approval before package updates, script execution, destination path changes, or agent registration.

Risk: The install script can move an existing destination aside and copy workspace assets into the selected path.

Mitigation: Run it only against the intended workspace and review the backup and destination paths before execution.

Risk: Broker-data access depends on a local Futu OpenD endpoint, and transport security is not established by the evidence.

Mitigation: Use only a local trusted Futu OpenD endpoint unless transport security is fixed.

Risk: Investment research and option-strategy outputs may be incorrect or unsuitable for a user's portfolio.

Mitigation: Treat generated approval packets as proposals and require human review before any trade or account action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gm4leejun-stack/skills/jun-invest-option-master-installer)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Futu OpenAPI documentation](https://openapi.futunn.com/futu-api-doc/intro/intro.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell commands, Python code, YAML/JSON configuration, and generated approval packet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deprecated installer; generated trading approval packets are proposals and require human approval before any action.]

## Skill Version(s):

0.99.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
