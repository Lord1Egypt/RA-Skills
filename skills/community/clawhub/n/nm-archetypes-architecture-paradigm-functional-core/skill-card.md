## Description: <br>
Applies Functional Core, Imperative Shell to isolate logic from side effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and software architects use this skill to evaluate whether Functional Core, Imperative Shell fits a codebase and to plan refactoring that separates pure business logic from I/O and framework side effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during broad architecture or testability discussions where Functional Core, Imperative Shell is not relevant. <br>
Mitigation: Confirm the codebase actually has business logic entangled with I/O or slow brittle tests before applying its recommendations. <br>
Risk: Refactoring toward immutable functional-core boundaries can add overhead in performance-critical paths. <br>
Mitigation: Avoid applying the pattern to hot paths unless profiling and a small proof of concept show acceptable cost. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with optional code examples and refactoring steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No tool execution or generated files are required by the skill.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
