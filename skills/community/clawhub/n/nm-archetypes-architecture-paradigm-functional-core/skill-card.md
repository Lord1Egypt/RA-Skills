## Description:

Applies Functional Core, Imperative Shell to isolate logic from side effects

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to separate business rules from I/O, making core logic easier to test and the imperative shell easier to change. It offers adoption steps, deliverables, and exit criteria for applying the pattern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business rules may drift into the imperative shell during refactoring.

Mitigation: Use a core-owns-decisions checklist in code reviews and enforce the boundary with architecture tests.

Risk: Framework lifecycle requirements may not fit the proposed shell adapters.

Mitigation: Build small proof-of-concept adapters to validate the integration approach before a large rewrite.

Risk: The pattern may add friction in performance-critical hot paths or teams without plans to adopt functional patterns.

Mitigation: Assess the fit for the target codebase and pilot the approach in a high-churn or critical module before expanding it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-functional-core)
- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose with adoption steps, deliverables, risks, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
