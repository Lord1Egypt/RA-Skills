## Description:

Manage mihomo (Clash Meta) proxy instances via REST API for status checks, proxy switching, delay tests, connection management, config reloads, restarts, cache flushing, and traffic or log monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasgao](https://clawhub.ai/user/jonasgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer Mihomo or Clash Meta proxy controllers, including inspecting status, choosing proxy nodes, testing latency, managing connections, reloading configuration, restarting service, clearing caches, and monitoring traffic or logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Mihomo live-control commands can disrupt proxy traffic, including restart, reload, cache flush, connection close, provider update, and upgrade actions.

Mitigation: Require explicit confirmation before disruptive operations and make the target controller and action clear before execution.

Risk: Bearer-token requests may be sent over plaintext HTTP to remote hosts.

Mitigation: Keep the controller bound to localhost or behind a trusted private or TLS connection, and avoid sending bearer secrets over plain HTTP to remote hosts.

## Reference(s):

- [Mihomo API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Mihomo controller URL and bearer secret; disruptive live-control actions should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
