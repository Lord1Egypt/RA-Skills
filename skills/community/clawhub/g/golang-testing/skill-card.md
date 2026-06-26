## Description: <br>
Guides agents in writing, reviewing, auditing, and debugging production-ready Go tests using table-driven tests, testify helpers and mocks, parallel tests, fuzzing, fixtures, goroutine leak detection, coverage, and integration-test patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to create and assess Go test suites, choose appropriate unit, integration, fuzz, mock, benchmark, and concurrency-test patterns, and diagnose flaky or failing tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read and edit Go project files, run Go-related test commands, and install the gotests helper. <br>
Mitigation: Review proposed file changes, generated tests, and tool installation commands before applying them. <br>
Risk: Integration-test examples may involve Docker Compose services or local databases. <br>
Mitigation: Review integration-test scaffolding and environment-specific commands before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-testing) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Test Helpers](references/helpers.md) <br>
- [HTTP Handler Testing](references/http-testing.md) <br>
- [Integration Testing](references/integration-testing.md) <br>
- [Mocking and Test Fixtures](references/mocking.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Go code examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, Go test commands, linter commands, dependency installation commands, and integration-test scaffolding for review before execution.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
