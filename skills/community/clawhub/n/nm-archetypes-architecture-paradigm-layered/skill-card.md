## Description: <br>
Provides layered n-tier architecture guidance for agents designing systems with clear presentation, application, domain, and persistence boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use when an agent needs to recommend or document a layered architecture, define layer responsibilities, set dependency rules, choose enforcement checks, or prepare architecture deliverables such as ADRs and dependency diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes broad activation wording, so the skill may appear in general architecture discussions where layered architecture is not the intended pattern. <br>
Mitigation: Use it for layered architecture, monolith separation, or related design tasks, and confirm that its recommendations fit the user's requested architecture style. <br>
Risk: Layered architecture guidance can become overly rigid or encourage pass-through code when applied without context. <br>
Mitigation: Review generated guidance against performance, scalability, and team workflow requirements before adopting layer boundaries or enforcement rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-archetypes-architecture-paradigm-layered) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Concise architecture guidance, ADR-ready notes, dependency-rule descriptions, tool recommendations, and review checklists.] <br>
**Output Parameters:** [System scope, target stack, desired layers, dependency constraints, compliance needs, and existing monolith or service boundaries.] <br>
**Other Properties Related to Output:** [The skill has no required runtime tools; it may recommend static analysis or architecture-test configuration for enforcing layer rules.] <br>

## Skill Version(s): <br>
1.9.12 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
