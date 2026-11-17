## Description:

Applies Functional Core, Imperative Shell to isolate logic from side effects

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to separate business rules from I/O, making core logic easier to test while the imperative shell handles side effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business logic can drift between the functional core and imperative shell.

Mitigation: Use a core-owns-decisions checklist in code reviews.

Risk: Framework lifecycle requirements may not fit the planned shell adapters.

Mitigation: Build small proof-of-concept adapters before committing to a broad rewrite.

Risk: Teams unfamiliar with the pattern may apply it inconsistently.

Mitigation: Use pair programming during adoption and document anti-patterns found in the pilot.

## Reference(s):

- [Night Market Archetypes project homepage (listed in skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-functional-core)

## Skill Output:

**Output Type(s):** [Guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture recommendations and adoption steps based on the user's stated context.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
