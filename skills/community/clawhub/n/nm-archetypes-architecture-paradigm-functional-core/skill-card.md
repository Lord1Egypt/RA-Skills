## Description: <br>
Applies Functional Core, Imperative Shell to isolate logic from side effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to separate pure business logic from side effects, improve testability with immutable domain models, and plan incremental adoption of a thin imperative shell. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to reorganize business logic, tests, adapters, or shell orchestration in a codebase. <br>
Mitigation: Review proposed refactors, run the relevant test suite, and scan changes before deployment. <br>
Risk: Functional-core boundaries can drift if business decisions are duplicated in the imperative shell. <br>
Mitigation: Use code review and architecture tests to keep decisions in the pure core and side effects in the shell. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-functional-core) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code, test, configuration, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable architecture guidance; proposed refactors should be reviewed before application.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
