## Description: <br>
Guides agents through designing and refactoring dependency injection in Go, including manual constructor injection and comparisons of google/wire, uber-go/dig, uber-go/fx, and samber/do. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to design Go service wiring, choose between manual constructor injection and DI libraries, and refactor tightly coupled code toward testable dependency boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated refactors, wiring changes, or Go and git commands could alter application behavior if applied without review. <br>
Mitigation: Review proposed changes and commands before approval, then run the relevant Go tests and linting in important repositories. <br>
Risk: Library-specific API examples can become stale as google/wire, uber-go/dig, uber-go/fx, or samber/do evolve. <br>
Mitigation: Check the linked official documentation before relying on exact API signatures or generated wiring patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-dependency-injection) <br>
- [Skill homepage](https://github.com/samber/cc-skills-golang) <br>
- [Manual Constructor Injection](references/manual-di.md) <br>
- [google/wire User Guide](https://github.com/google/wire/blob/main/docs/guide.md) <br>
- [samber/do documentation](https://do.samber.dev) <br>
- [uber-go/fx documentation](https://uber-go.github.io/fx/) <br>
- [uber-go/dig](https://github.com/uber-go/dig) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Go file edits, DI library choices, tests, linting, and Go or git commands.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
