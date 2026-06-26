## Description: <br>
Guides agents in writing and reviewing Go tests that use stretchr/testify, including assertions, mocks, suites, async polling, and common pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to write or review Go tests in projects that import github.com/stretchr/testify. It helps choose assert versus require, build mocks, structure suites, verify expectations, and avoid common testify mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited tests may contain incorrect or misleading assertions. <br>
Mitigation: Review generated changes, run Go test tooling, and scan the resulting code before committing. <br>
Risk: The workflow can use the disclosed gotests dependency as a third-party Go tool. <br>
Mitigation: Install gotests only in approved development environments and treat it as a normal third-party Go dependency. <br>


## Reference(s): <br>
- [Mock reference](references/mock.md) <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-stretchr-testify) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Go code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or modify Go test files and run disclosed Go-related tooling when the agent has permission.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
