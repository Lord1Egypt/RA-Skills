## Description:

Scholarly literature and bibliographic databases: OpenAlex, Crossref, Europe PMC, PubMed, DOAJ, DBLP, and Semantic Scholar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, academic analysts, librarians, and developers use this skill to discover scholarly metadata, bibliographic records, and citation, funder, and institution graph data through Pilot Protocol service agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries or identifiers may be sent to external academic agents and a summary provider.

Mitigation: Use only trusted Pilot Protocol daemons and networks, and avoid submitting confidential research queries or private identifiers unless that sharing is acceptable.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-academic)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon joined to network 9, and the list-agents directory agent reachable on the overlay.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
