## Description:

Modular monolith with enforced internal boundaries. Use for service-level autonomy without a distributed system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to define module boundaries and contracts in a monolithic codebase, maintain team autonomy, and assess when a module may be ready to become a separate service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Without consistent enforcement, internal module boundaries may erode and dependencies can become tangled.

Mitigation: Make boundary violations build-breaking and review dependencies regularly.

Risk: A shared database can become a contention hotspot and couple modules through their data access.

Mitigation: Define schema ownership, restrict visibility, and consider replication where appropriate.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-modular-monolith)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown architectural guidance, recommendations, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes module boundaries, contracts, enforcement practices, and exit criteria.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
