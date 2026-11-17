## Description:

Route HTTP requests through Pilot Protocol tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route HTTP traffic through Pilot Protocol tunnels, including services behind NATs or firewalls and local HTTP servers exposed to remote agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway mappings can route or expose internal HTTP services over the Pilot overlay network.

Mitigation: Map only services you intend to expose or route, and verify authentication and access controls on those services before use.

Risk: Using privileged HTTP ports on Linux may require root or sudo.

Mitigation: Avoid privileged ports unless elevated access is necessary and understood.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-http-proxy)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilot-protocol skill, a running Pilot daemon, and the pilotctl binary on PATH.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
