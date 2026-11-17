## Description:

Helps agents guide Go developers using samber/ro to design reactive streams, choose operators and subjects, and write event-driven pipelines with cancellation, error handling, and plugin usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when adopting or maintaining Go code that imports github.com/samber/ro or needs asynchronous, event-driven, or real-time stream processing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated application code may use samber/ro plugins for HTTP, filesystem watching, cron scheduling, signals, or process integration.

Mitigation: Review generated code for appropriate paths, timeouts, retry limits, and operational permissions before applying it.

Risk: Long-running or infinite streams can continue running if cancellation or completion is omitted.

Mitigation: Use context cancellation, TakeUntil, Timeout, Unsubscribe, Complete, or Error to bound stream lifecycles.

Risk: Observer code that omits error handling can hide stream failures.

Mitigation: Prefer NewObserver with onNext, onError, and onComplete callbacks for subscriptions that may fail.

Risk: Untyped Pipe usage can lose compile-time type checking in Go pipelines.

Mitigation: Prefer typed Pipe functions such as Pipe2 through Pipe25 when composing operator chains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-samber-ro)
- [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang)
- [samber/ro GitHub repository](https://github.com/samber/ro)
- [samber/ro documentation](https://ro.samber.dev)
- [pkg.go.dev github.com/samber/ro](https://pkg.go.dev/github.com/samber/ro)
- [ReactiveX](https://reactivex.io/)
- [Operators Guide](references/operators-guide.md)
- [Reactive Patterns](references/patterns.md)
- [Plugin Ecosystem](references/plugin-ecosystem.md)
- [Subjects Guide](references/subjects-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Go code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference optional samber/ro plugins and Go tooling when relevant to the user's codebase.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
