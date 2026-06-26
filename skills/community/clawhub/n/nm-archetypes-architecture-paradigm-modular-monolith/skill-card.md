## Description: <br>
Applies modular monolith with enforced internal boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and software architecture teams use this skill to organize large monolithic codebases into well-bounded modules with explicit internal contracts, dependency checks, and a path toward future service extraction when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated refactoring, CI boundary checks, or ADR changes could affect downstream code or architecture if applied without review. <br>
Mitigation: Review proposed refactoring, boundary checks, and ADR updates before applying them, and scan downstream code changes through the project review process. <br>
Risk: Module boundaries can erode over time if dependency rules are documented but not enforced. <br>
Mitigation: Use automated dependency checks and treat boundary violations as build-breaking issues. <br>
Risk: Shared database ownership can create coupling and contention across modules. <br>
Mitigation: Define schema ownership and public data access contracts before introducing shared database interactions between modules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-archetypes-architecture-paradigm-modular-monolith) <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Code] <br>
**Output Format:** [Markdown architecture guidance with ADR, contract documentation, dependency-check, and CI boundary-enforcement recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code or hidden access paths were identified in security evidence.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
