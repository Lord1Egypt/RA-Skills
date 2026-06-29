## Description: <br>
Applies hexagonal architecture isolating domain from infrastructure <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and architecture reviewers use this skill to apply hexagonal architecture, define ports and adapters, separate domain logic from infrastructure, and plan contract testing for systems with swappable dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The architecture guidance may add unnecessary port and adapter abstraction to small scripts or prototypes. <br>
Mitigation: Use the skill for systems that need infrastructure independence or contract-tested integrations, and avoid applying it to small utilities without external dependencies. <br>
Risk: Port interfaces can become too granular or expose transport details. <br>
Mitigation: Group related operations around domain aggregates and keep port data structures domain-centered rather than tied to HTTP, database, or framework concerns. <br>
Risk: Adapters can drift from the external systems they represent. <br>
Mitigation: Maintain automated contract tests and validation checks that confirm adapters still satisfy their port expectations as schemas or APIs change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-hexagonal) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with architecture steps, deliverables, and implementation vocabulary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter: 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
