## Description: <br>
Monadic types for Golang using samber/mo: Option, Result, Either, Future, IO, Task, and State types for type-safe nullable values, error handling, and functional composition with pipeline sub-packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when working with Go projects that use or are adopting github.com/samber/mo for monadic nullable values, composable error handling, discriminated unions, and functional pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may make the skill relevant during general Go error-handling or nil-safety discussions even when the project is not adopting samber/mo. <br>
Mitigation: Use it when samber/mo is already present or intentionally being evaluated, and review any dependency additions before applying them. <br>
Risk: Suggested code edits may introduce incorrect monadic wrapping, unwrapping, or dependency changes. <br>
Mitigation: Review proposed code changes and run the project's Go tests and linters before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-samber-mo) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Homepage](https://github.com/samber/cc-skills-golang) <br>
- [pkg.go.dev github.com/samber/mo](https://pkg.go.dev/github.com/samber/mo) <br>
- [samber/mo GitHub repository](https://github.com/samber/mo) <br>
- [Advanced Types Reference](references/advanced-types.md) <br>
- [Either Reference](references/either.md) <br>
- [Monads Guide](references/monads-guide.md) <br>
- [Option Reference](references/option.md) <br>
- [Pipelines Reference](references/pipelines.md) <br>
- [Result Reference](references/result.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Go and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Go dependency additions, code edits, and usage patterns for samber/mo.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
