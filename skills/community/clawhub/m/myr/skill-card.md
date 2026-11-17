## Description:

MYR helps agents capture, search, verify, export, import, and synthesize Methodological Yield Reports for OODA-based intelligence compounding across nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordangreenhall](https://clawhub.ai/user/jordangreenhall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use MYR to install and operate a signed methodological-yield reporting system, search past yield, verify report quality, and sync reviewed reports between trusted nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running mutable external installer code.

Mitigation: Use a pinned download or clone, inspect the installer, and verify checksums or signatures before running commands.

Risk: The skill can configure a persistent peer-sync server.

Mitigation: Restrict network reachability, know how to disable the service, and expose the server only in a trusted network environment.

Risk: Peer auto-approval can trust remote nodes without manual operator review.

Mitigation: Leave peer auto-approval disabled unless the network is trusted, and verify peer fingerprints out of band before approval.

Risk: Shared reports and node metadata may become reachable to approved peers.

Mitigation: Mark only reviewed reports as shareable and use explicit peer approval before syncing data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jordangreenhall/skills/myr)
- [MYR system repository declared by the artifact](https://github.com/JordanGreenhall/myr-system)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For each MYR operation, the skill asks the agent to report the action performed, affected artifact IDs, verification result, and next recommended step.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
