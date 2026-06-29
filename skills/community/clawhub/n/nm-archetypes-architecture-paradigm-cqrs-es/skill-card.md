## Description: <br>
Applies CQRS and Event Sourcing for read/write separation and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architects use this skill to decide when CQRS and Event Sourcing fit systems with complex domain logic, separate read/write workloads, durable audit trails, projections, and event replay needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CQRS and Event Sourcing can add operational complexity when applied to simple CRUD or small systems. <br>
Mitigation: Use the skill's fit criteria before adoption and avoid these patterns when the system does not need complex domain logic, separate scaling, or a full audit trail. <br>
Risk: Eventual consistency can make user-visible state lag behind accepted commands. <br>
Mitigation: Define read-model update expectations and provide immediate command-side feedback where user experience depends on timely confirmation. <br>
Risk: Event schema changes can break projections or consumers. <br>
Mitigation: Document schema versioning, use validation gates, and plan migration or replay tooling before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-cqrs-es) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown architecture guidance with adoption steps, deliverables, component vocabulary, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no tools, credentials, API keys, or actions are requested.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
