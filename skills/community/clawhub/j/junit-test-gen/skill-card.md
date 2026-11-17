## Description:

Generates JUnit 5 test classes from JSON test case files. Invoke when user wants to generate Spring Boot JUnit 5 tests from JSON test cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hcyyy0120](https://clawhub.ai/user/hcyyy0120)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to convert structured JSON test cases into Spring Boot JUnit 5 test classes, including request setup, assertions, and optional setup or teardown SQL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill generates project files and executable Java tests from JSON input with insufficient containment and escaping.

Mitigation: Use only trusted JSON test cases, write output to a controlled test directory, and inspect generated Java before compiling or running it.

Risk: Generated tests can execute setup and teardown SQL against a configured database.

Mitigation: Run generated tests only against disposable test databases with restricted credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hcyyy0120/skills/junit-test-gen)
- [Publisher profile](https://clawhub.ai/user/hcyyy0120)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Generated Java test files with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tests should be reviewed before compiling or running.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
