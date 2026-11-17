## Description:

Applies client-server architecture for web/mobile apps

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to plan client-server or peer-to-peer systems, define trust boundaries and API contracts, manage client-server version skew, and account for intermittent connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chatty clients can create avoidable latency and poor performance.

Mitigation: Consolidate requests behind a facade or gateway and use client-side or edge caching where appropriate.

Risk: Duplicated business logic across clients can become inconsistent with server behavior.

Mitigation: Keep rules on the server or share validation through a common library.

Risk: Peer-to-peer updates can conflict when devices change data independently.

Mitigation: Define a conflict-resolution approach, such as CRDTs, last-write-wins, or consensus, during design.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-client-server)
- [Related project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown architecture guidance, recommendations, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the described system; covers client-server and, where relevant, peer-to-peer design considerations.]

## Skill Version(s):

1.10.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
