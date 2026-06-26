## Description: <br>
Generates JUnit 5 test classes from JSON test case files for Spring Boot projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hcyyy0120](https://clawhub.ai/user/hcyyy0120) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to convert trusted JSON test-case suites into Spring Boot JUnit 5 tests, including controller/API test scaffolding and optional setup/teardown SQL from the input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tests can execute SQL from JSON input against a Spring database without strong safety limits. <br>
Mitigation: Use only trusted JSON test-case files, review generated Java before compiling or running it, and run Maven with an isolated test profile and disposable database. <br>
Risk: Setup or teardown SQL in test-case JSON may contain destructive statements. <br>
Mitigation: Check SQL for destructive operations such as DROP, TRUNCATE, ALTER, broad DELETE, or UPDATE before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/hcyyy0120/junit-test-gen) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, guidance] <br>
**Output Format:** [Generated Java test code and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated tests may include setup and teardown SQL from the provided JSON test cases.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
