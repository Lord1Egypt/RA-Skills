## Description:

Ops Hygiene provides standard operating procedures and shell scripts for agent maintenance, security hygiene, system health checks, secret scanning, security audits, and recurring housekeeping tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staybased](https://clawhub.ai/user/staybased)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run recurring OpenClaw workspace maintenance, including health checks, secret scans, security audits, heartbeat triage, memory upkeep, and dependency review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review says the skill mixes routine health checks with automatic email and API-key use.

Mitigation: Before enabling recurring heartbeat use, remove or configure the hard-coded AgentMail inbox and require explicit consent before reading secrets from .secrets.

Risk: The bundled scripts inspect the OpenClaw workspace and parts of the host environment.

Mitigation: Run the scripts only in approved workspaces and restrict audit paths to locations the operator has authorized.

Risk: The server security guidance says bundled security-audit results should be treated as advisory until script bugs are fixed.

Mitigation: Validate the audit scripts in a staging workspace and manually review findings before using them for security decisions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/staybased/skills/ops-hygiene)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, text]

**Output Format:** [Markdown guidance with bash commands plus JSON or text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may inspect local workspace and host state, call local services, and write heartbeat state under workspace memory.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
