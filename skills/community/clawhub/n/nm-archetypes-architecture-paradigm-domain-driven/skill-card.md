## Description:

Models a business in its own language

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to model business domains in the language of domain experts, identify bounded contexts, and choose domain structures as real needs emerge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared type can expose unintended fields when it crosses an IO boundary.

Mitigation: Audit the fields of every type that crosses an IO boundary, and use a separately versioned request DTO when independently deployed systems need to evolve command shapes.

Risk: Adding DTOs, mappers, or layers without a current need can add ceremony without improving the model.

Mitigation: Document the need that justifies each abstraction and remove mappings that only copy fields one-to-one.

Risk: A domain model can become anemic when business rules live only in services.

Mitigation: Keep behavior with the domain objects that own the rules, or recognize when the domain does not need DDD.

## Reference(s):

- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)
- [SE-Radio Episode 226: Eric Evans on Domain-Driven Design at 10 Years](https://www.youtube.com/watch?v=GogQor9WG-c)
- [The Core of Domain-Driven Design](https://www.angulararchitects.io/en/blog/the-core-of-domain-driven-design/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance and planning artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of a domain glossary, context map, architecture decision record, and IO-boundary field audit.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
