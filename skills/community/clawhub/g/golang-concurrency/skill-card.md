## Description: <br>
Golang concurrency patterns. Use when writing or reviewing concurrent Go code involving goroutines, channels, select, locks, sync primitives, errgroup, singleflight, worker pools, or fan-out/fan-in pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to implement, review, and audit concurrent Go code for goroutine lifecycle, channel ownership, synchronization, worker-pool, pipeline, and race-condition issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to modify Go code and run Go or git commands. <br>
Mitigation: Use it in repositories where coding-agent permissions are acceptable, review diffs before merge, and run the project's Go tests and lint checks. <br>
Risk: Concurrency changes can introduce races, goroutine leaks, deadlocks, or misleading fixes if applied without validation. <br>
Mitigation: Validate changes with focused code review, cancellation and lifecycle tests, race detection where practical, and leak checks for goroutine-heavy code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-concurrency) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Channels and Select Patterns](references/channels-and-select.md) <br>
- [Pipelines and Worker Pools](references/pipelines.md) <br>
- [Sync Primitives Deep Dive](references/sync-primitives.md) <br>
- [Go Concurrency Patterns: Pipelines](https://go.dev/blog/pipelines) <br>
- [Effective Go: Concurrency](https://go.dev/doc/effective_go#concurrency) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown prose with Go code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to edit Go code and run go, golangci-lint, or git commands.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
