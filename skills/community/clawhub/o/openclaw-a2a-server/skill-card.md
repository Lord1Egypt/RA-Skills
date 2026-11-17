## Description:

Run an A2A inbound task listener that lets this OpenClaw instance receive tasks from other agents via the A2A API Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thearchitectit](https://clawhub.ai/user/thearchitectit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to start, stop, and check an OpenClaw sidecar listener that receives inbound A2A tasks from a gateway and invokes the local OpenClaw instance for responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The listener can receive remote inbound tasks, and authentication is disabled when no A2A_GATEWAY_API_KEY is configured.

Mitigation: Use only on a trusted host and trusted network, set a strong A2A_GATEWAY_API_KEY, and avoid binding to 0.0.0.0 unless firewall or gateway controls protect the service.

Risk: Configuring A2A_OPENCLAW_COMMAND enables command-based invocation from task content handled by the listener.

Mitigation: Do not enable A2A_OPENCLAW_COMMAND for normal deployments; prefer the fixed OpenClaw CLI path or a locked-down HTTPS backend.

Risk: Listener logs and configuration may contain sensitive task or credential material.

Mitigation: Treat a2a-listener.log and a2a.conf as sensitive files and restrict local filesystem access to trusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thearchitectit/skills/openclaw-a2a-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or stop a local background HTTP listener and write PID and log files when the suggested commands are executed.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
