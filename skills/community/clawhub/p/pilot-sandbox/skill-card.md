## Description:

Pilot Sandbox helps agents bring a Pilot Protocol node online from a network-restricted sandbox by routing Pilot TLS endpoints through an HTTPS proxy and running pilot-daemon in compat mode inside a private mount namespace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a Pilot Protocol node must register from a locked-down hosted VM or sandbox where UDP is blocked, direct DNS or TCP egress is unreliable, and only HTTPS CONNECT through a proxy is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts privileged background network routing and runs pilot-daemon in a private mount namespace.

Mitigation: Use it only in a disposable VM or tightly scoped environment, and stop the router and daemon processes when finished.

Risk: The workaround depends on an HTTPS proxy for outbound connectivity.

Mitigation: Confirm HTTPS_PROXY points to a trusted proxy before starting the router.

Risk: The pinned certificate fallback can be unsafe if the fingerprint is refreshed from an untrusted channel.

Mitigation: Prefer system TLS trust, and use certificate pinning only after verifying the fingerprint through an independent trusted channel.

## Reference(s):

- [Pilot firewalls and compat mode](https://pilotprotocol.network/docs/firewalls)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot locked-down sandbox blog](https://pilotprotocol.network/blog/pilot-protocol-from-a-locked-down-agent-sandbox)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-sandbox)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash code blocks and bundled shell/Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational setup steps for root or CAP_SYS_ADMIN environments with HTTPS_PROXY configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
