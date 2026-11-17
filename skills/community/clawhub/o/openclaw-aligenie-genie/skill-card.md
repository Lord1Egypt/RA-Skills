## Description:

OpenClaw Agent uses a cloud server to communicate bidirectionally with Tmall Genie, including receiving messages, configuring the connection, and handling commands sent from Tmall Genie to OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect an OpenClaw agent with a self-managed Aligenie/Tmall Genie relay service, register agents, poll for user requests, and submit voice-assistant replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment examples show public plain-HTTP endpoints for a relay service that uses API keys and device or agent management operations.

Mitigation: Use a trusted self-managed server behind HTTPS, restrict firewall access, and avoid sending real credentials to the documented plain-HTTP examples.

Risk: The deployment guide includes an Administrator scheduled task from C:\temp and management endpoints that can create or delete devices, agents, and keys.

Mitigation: Run the service with least privilege, store it outside temporary directories, scope API keys narrowly, and confirm server-side permissions before enabling management endpoints.

Risk: The deployment flow depends on manually downloaded server dependencies.

Mitigation: Pin and verify downloaded dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/openclaw-aligenie-genie)
- [Technical specification](SPEC.md)
- [Deployment guide](DEPLOY.md)
- [SQLite JDBC releases](https://github.com/xerial/sqlite-jdbc/releases)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variables, API key usage patterns, deployment commands, and a Python client for polling and submitting results.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
