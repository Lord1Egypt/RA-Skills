## Description:

Production-ready Golang tests: table-driven tests, testify suites and mocks, parallel tests, fuzzing, fixtures, goroutine leak detection with goleak, snapshot testing, code coverage, integration tests, and idiomatic test naming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to write, review, audit, and debug Go tests. It guides agents toward maintainable unit, integration, fuzz, benchmark, HTTP, mock, and concurrency tests for Go projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may edit Go test files or suggest Go commands that change project behavior.

Mitigation: Review generated test changes and run the relevant Go test commands before merging.

Risk: Integration-test guidance may involve Docker Compose fixtures, databases, local services, ports, volumes, or cleanup steps.

Mitigation: Review fixture configuration and isolate credentials, ports, volumes, and data before running integration tests.

Risk: Installing gotests or clockwork with unpinned versions can introduce changing tool behavior.

Mitigation: Pin tool and dependency versions in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-testing)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Test Helpers](references/helpers.md)
- [HTTP Handler Testing](references/http-testing.md)
- [Integration Testing](references/integration-testing.md)
- [Mocking and Test Fixtures](references/mocking.md)
- [gotests dependency](https://github.com/cweill/gotests)
- [testify timeout helper discussion](https://github.com/stretchr/testify/issues/1101)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Go code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit or propose Go test files, mocks, fixtures, build tags, and test-running commands.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
