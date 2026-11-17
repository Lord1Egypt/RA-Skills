## Description:

Golang concurrency patterns. Use when writing or reviewing concurrent Go code involving goroutines, channels, select, locks, sync primitives, errgroup, singleflight, worker pools, or fan-out/fan-in pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to write, review, and audit concurrent Go code for goroutine lifecycle, cancellation, channel ownership, synchronization, worker pools, and pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests unrestricted Git command access that can change repository state beyond the stated need.

Mitigation: Use the skill in a clean working tree, keep valuable uncommitted work and remote credentials out of scope, and narrow Git access to read-only commands unless mutation is explicitly required.

Risk: The skill can propose or apply edits to Go source files while addressing concurrency issues.

Mitigation: Review generated code changes, run Go tests with the race detector where practical, and confirm concurrency behavior before merging.

## Reference(s):

- [cc-skills-golang repository](https://github.com/samber/cc-skills-golang)
- [Channels and Select Patterns](references/channels-and-select.md)
- [Pipelines and Worker Pools](references/pipelines.md)
- [Sync Primitives Deep Dive](references/sync-primitives.md)
- [Go Concurrency Patterns: Pipelines](https://go.dev/blog/pipelines)
- [Effective Go: Concurrency](https://go.dev/doc/effective_go#concurrency)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, markdown]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend repository edits and Go tooling commands when the harness grants access.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
