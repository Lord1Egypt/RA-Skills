## Description:

Generates JUnit 5 and Mockito unit tests for Java/Maven source code, including full class test generation and incremental updates for changes on a git branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or update JUnit 5 and Mockito unit tests for Java/Maven projects, especially when they need targeted coverage for changed classes and methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or updated unit tests may encode incorrect assumptions about business logic.

Mitigation: Review generated tests against the source behavior and run the relevant Maven test commands before accepting changes.

Risk: Dependency suggestions or pom.xml edits may affect build compatibility, especially across Java 8 and Java 11+ Mockito versions.

Mitigation: Require user confirmation before pom.xml changes and verify with Maven test compilation after dependency updates.

Risk: The skill reads project source, runs git and Maven checks, and may create test files in the target repository.

Mitigation: Use it in trusted workspaces and review the file diff before committing generated tests.

## Reference(s):

- [Dependency Configuration Reference](artifact/references/dependency-config.md)
- [JUnit 5 and Mockito Test Template Reference](artifact/references/test-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Java test code, Maven XML snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Java test files and, with user confirmation, Maven pom.xml test dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
