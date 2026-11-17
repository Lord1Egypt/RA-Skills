## Description:

Provides developer-platform metadata for GitHub, Docker Hub, crates.io, and other ecosystem registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and engineers use this skill to discover and query public developer-platform metadata, including public repository details, package registry data, container image search results, and ecosystem activity. It is intended for read-only metadata workflows through Pilot Protocol service agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may expose private repository names, credentials, or sensitive terms to public developer-platform metadata agents.

Mitigation: Use only public, non-sensitive queries and avoid sending credentials, private repository names, or confidential project details.

Risk: The skill has a documentation scope mismatch around npm and package-registry coverage.

Mitigation: Confirm the target service agent with list-agents and /help before routing npm or package-registry questions.

Risk: The skill requires Pilot Protocol network 9, pilotctl, a running daemon, and reachable service agents.

Mitigation: Verify the daemon, network join, pilotctl availability, and agent contract before relying on returned metadata.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-dev)
- [Publisher skill index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses depend on Pilot Protocol service agents, pilotctl, and public upstream metadata availability.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
