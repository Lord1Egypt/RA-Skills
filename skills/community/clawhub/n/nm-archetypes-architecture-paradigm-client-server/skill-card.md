## Description:

Applies client-server architecture for web/mobile apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to plan client-server or peer-to-peer systems, define trust boundaries and API contracts, and document versioning, connectivity, and rollout decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frequent small client requests can hurt performance.

Mitigation: Consolidate API calls through a façade or gateway and use client-side or edge caching.

Risk: Duplicated business logic in clients can drift out of sync with server rules.

Mitigation: Share validation logic in a common library or make the server the definitive owner of those rules.

Risk: Peer-to-peer synchronization can produce conflicting data updates.

Mitigation: Choose and document a conflict-resolution approach, such as CRDTs or last-write-wins, before implementation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-client-server)
- [Publisher profile](https://clawhub.ai/user/athola)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture recommendations and documentation outlines, including ADR, API or protocol specification, compatibility criteria, and rollout runbook guidance.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
