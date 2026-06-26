## Description: <br>
Run mutation testing to measure real test suite effectiveness by injecting code mutations, running tests against mutants, and reporting mutation score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate whether a test suite catches realistic defects, identify survived mutants, and generate targeted tests for uncovered behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutation testing may temporarily modify source files while evaluating whether tests catch changed behavior. <br>
Mitigation: Run it on a clean branch, disposable checkout, or container, and verify that all mutations are reverted before continuing development. <br>
Risk: The skill may install and run ecosystem mutation-testing tools such as Stryker, mutmut, PIT, or gremlins. <br>
Mitigation: Review package installs and dependency changes before execution, especially in restricted or production-adjacent environments. <br>
Risk: Project tests may be configured to contact production services or use real credentials. <br>
Mitigation: Run with isolated test configuration, test endpoints, and non-production credentials only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/mutation-test-runner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mutation score summaries, survived-mutant analysis, and concrete test suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
