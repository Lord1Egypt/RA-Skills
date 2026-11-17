## Description:

Models a business in its own language

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and domain experts use this skill to define ubiquitous language and bounded contexts, decide when domain-driven design fits, and evolve systems without adding architecture ceremony prematurely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared data types can expose fields unintentionally across network or other IO boundaries.

Mitigation: Audit the fields of every type crossing an IO boundary; use versioned request DTOs when independently deployed systems need to evolve their contracts.

Risk: Adding DTOs, mappers, or layers without a current need can create unnecessary ceremony.

Mitigation: Record the concrete need for each added boundary or translation, and defer the split until the view contract and domain model diverge.

Risk: A domain model with no behavior can become a renamed schema while business rules remain elsewhere.

Mitigation: Place rules on the domain objects that own them, or use a simpler model when the domain does not need DDD.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-domain-driven)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)
- [SE-Radio Episode 226: Eric Evans on Domain-Driven Design at 10 Years](https://www.youtube.com/watch?v=GogQor9WG-c)
- [The Core of Domain-Driven Design](https://www.angulararchitects.io/en/blog/the-core-of-domain-driven-design/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose and structured lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides adoption steps, design recommendations, and review criteria; no fixed output template.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
