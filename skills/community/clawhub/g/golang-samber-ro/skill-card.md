## Description: <br>
Reactive streams and event-driven programming in Golang using samber/ro, a ReactiveX implementation with type-safe operators, cold and hot observables, subject types, plugins, backpressure, error propagation, and Go context integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adopting or maintaining Go code that imports github.com/samber/ro or when designing asynchronous event-driven pipelines, real-time streams, hot observables, subjects, and reactive architectures. It also helps distinguish stream-oriented samber/ro use cases from finite slice transformations that are better served by samber/lo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reactive streams that are not bounded or cancelled can continue running and consume resources. <br>
Mitigation: Use the skill's guidance on Take, TakeUntil, Timeout, context cancellation, Wait, and Unsubscribe for long-lived or infinite streams. <br>
Risk: Subscription code that omits error and completion handlers can hide stream failures. <br>
Mitigation: Prefer observers with onNext, onError, and onComplete callbacks, and surface errors through logging or application-specific handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-samber-ro) <br>
- [ClawHub Metadata Homepage](https://github.com/samber/cc-skills-golang) <br>
- [samber/ro GitHub Repository](https://github.com/samber/ro) <br>
- [samber/ro Documentation](https://ro.samber.dev) <br>
- [pkg.go.dev samber/ro](https://pkg.go.dev/github.com/samber/ro) <br>
- [ReactiveX](https://reactivex.io/) <br>
- [Operators Guide](references/operators-guide.md) <br>
- [Reactive Patterns](references/patterns.md) <br>
- [Plugin Ecosystem](references/plugin-ecosystem.md) <br>
- [Subjects Guide](references/subjects-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Go code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Go tooling, samber/ro APIs, and optional Context7 documentation lookup when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
