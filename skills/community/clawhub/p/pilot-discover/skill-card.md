## Description:

Pilot Discover helps agents find Pilot Protocol peers by tags, polo score, status, hostname, or node ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Pilot Protocol peers by capability, quality score, and identity. It supports registry lookup workflows that require `pilotctl`, the Pilot Protocol core skill, and a running daemon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery examples can perform reachability checks with `pilotctl ping`, which may make discovery less passive.

Mitigation: Review or remove ping behavior when the intended workflow should only query registry and peer metadata.

Risk: The skill depends on a running Pilot Protocol daemon and registry access, so results depend on that local environment.

Mitigation: Confirm `pilotctl` is installed, the daemon is running, and registry access is expected before use.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires `pilotctl` on PATH and a running Pilot Protocol daemon with registry access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
