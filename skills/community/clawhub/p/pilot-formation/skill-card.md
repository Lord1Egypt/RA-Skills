## Description:

Deploy predefined network topologies (star, ring, mesh, tree) for structured swarms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and engineers use this skill to form structured Pilot Protocol swarms with star, ring, mesh, tree, or line communication patterns when connection overhead or hierarchy needs to be controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pending peer trust requests may be approved too broadly during topology formation.

Mitigation: Verify pending peer identities before approval and avoid approving unrelated pending handshakes.

Risk: Publishing topology details to a registry can expose swarm layout information.

Mitigation: Remove the publishing step or explicitly configure it only when topology details are intended to be shared.

Risk: The skill can change peer trust and network topology in a live Pilot environment.

Mitigation: Review before installing and use it only in a controlled pilot environment.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-formation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilotctl binary, jq, the pilot-protocol skill, and a running Pilot daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
