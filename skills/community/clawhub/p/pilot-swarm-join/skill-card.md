## Description:

Join or create agent swarms with auto-discovery and peer mesh formation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to join or create named Pilot Protocol swarms, discover peers, and establish mesh trust with intended swarm members.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval examples can approve every pending peer connection rather than only verified swarm members.

Mitigation: List pending requests, verify each node against the intended swarm and registry, and approve peers one at a time.

Risk: Using an untrusted registry or unknown swarm members can establish trust with unintended nodes.

Mitigation: Use trusted registries and known swarm members, and do not run blanket approval commands where unrelated handshake requests may be pending.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-swarm-join)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, a running Pilot Protocol daemon, and a registry connection.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
