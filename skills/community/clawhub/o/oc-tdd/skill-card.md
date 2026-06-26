## Description: <br>
A Test-Driven Development assistant that generates test cases from code or specifications, runs tests, tracks coverage, guides the red-green-refactor cycle, and supports pytest, unittest, jest, and go test. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and run tests, inspect coverage, and follow a red-green-refactor workflow across supported project test frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running tests can execute code from the target project. <br>
Mitigation: Use the skill only on trusted projects and review generated commands before execution. <br>
Risk: Some advertised workflow, mutation, Jest, or Go capabilities may need verification before use. <br>
Mitigation: Confirm the required framework support in the artifact and test it in a controlled project before depending on those paths. <br>
Risk: Temporary test report files use predictable /tmp paths on shared machines. <br>
Mitigation: Run in an isolated workspace or clean up temporary reports after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/oc-tdd) <br>
- [Publisher profile](https://clawhub.ai/user/michealxie001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated test code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated tests or coverage reports when users run the provided commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
