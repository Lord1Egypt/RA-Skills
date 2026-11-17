## Description:

Manages local IPFS file pins for OpenClaw, tracking expiration and removing unused content after its TTL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to add and retrieve files through a local IPFS node, maintain active pins, and automatically remove expired pins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expired or manually removed pins followed by garbage collection can make locally stored content unavailable.

Mitigation: Keep backups or redundant pins for important CIDs; preview expiration with decay --dry-run and refresh active pins before their TTL ends.

## Reference(s):

- [Ipfs Pin Stage on ClawHub](https://clawhub.ai/paradoxfuzzle/skills/ipfs-pin)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [Plain text or JSON status and CIDs; retrieved file content when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only CIDs and status returned by the local IPFS CLI.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
