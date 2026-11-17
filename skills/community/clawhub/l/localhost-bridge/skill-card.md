## Description:

Bridge Docker containers to host localhost services via socat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superworldsavior](https://clawhub.ai/user/superworldsavior)

### License/Terms of Use:


## Use Case:

Developers and administrators use this skill to let selected Docker containers reach host services bound to 127.0.0.1, such as AI gateways, MCP servers, Ollama, databases, or cache services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent network bridge can expose a host-local service to containers beyond the intended scope.

Mitigation: Use the skill only when an administrator intentionally wants one Docker network to reach one specific localhost service, and review the generated systemd unit before enabling it.

Risk: An incorrect bind address or firewall rule can make the service reachable from places the administrator did not intend.

Mitigation: Confirm the bridge IP, service port, and UFW interface rule before running commands, then test that the service is not publicly reachable.

Risk: Forwarded services may become accessible without enough application-level protection.

Mitigation: Confirm the target service has its own authentication or access controls before exposing it through the bridge.

## Reference(s):

- [Localhost Bridge on ClawHub](https://clawhub.ai/superworldsavior/skills/localhost-bridge)
- [The Localhost Trap](https://casys.ai/blog/the-localhost-trap)
- [Docker packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for manual administrator review before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
