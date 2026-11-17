## Description:

Book search and catalogs for Project Gutenberg through Gutendex and Open Library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover book-search service agents, inspect their filter contracts, and query Project Gutenberg or Open Library for book metadata and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book-search queries and free-text summary requests may be sent over the Pilot Protocol overlay to remote service agents.

Mitigation: Avoid including private or sensitive text in search, summary, or free-text requests.

Risk: The available service-agent catalogue and each agent's filter contract can change over time.

Mitigation: Query list-agents and read an agent's /help response before relying on a specific hostname or filter schema.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-books)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and reachable service agents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
