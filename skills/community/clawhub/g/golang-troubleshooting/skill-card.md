## Description:

Troubleshoot Golang programs systematically - find and fix the root cause. Use when encountering bugs, crashes, deadlocks, or unexpected behavior in Go code. Covers debugging methodology, common Go pitfalls, test-driven debugging, pprof setup and capture, Delve debugger, race detection, GODEBUG tracing, and production debugging. Start here for any 'something is wrong' situation. Not for interpreting profiles or benchmarking (-> See `samber/cc-skills-golang@golang-benchmark` skill) or applying optimization patterns (-> See `samber/cc-skills-golang@golang-performance` skill).

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate Go bugs, crashes, hangs, race conditions, performance symptoms, build failures, and production incidents with a root-cause-first workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production debugging guidance can expose secrets, sensitive traffic, logs, profiles, database contents, or environment values if used without safeguards.

Mitigation: Require explicit approval for pprof captures, full HTTP dumps, database queries, and environment inspection; redact secrets, restrict log and profile access, and use HTTPS or tunnels for remote diagnostics.

Risk: The skill can guide code edits and Go, git, and Delve command execution during troubleshooting.

Mitigation: Review proposed changes and commands before execution, run diagnostics in least-privilege environments when possible, and pin installed tool versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-troubleshooting)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [General Debugging Methodology](references/methodology.md)
- [Common Go Bugs](references/common-go-bugs.md)
- [Test-Driven Debugging](references/testing-debug.md)
- [Concurrency Debugging](references/concurrency-debug.md)
- [Performance Troubleshooting](references/performance-debug.md)
- [pprof Reference](references/pprof.md)
- [Diagnostic Tools](references/diagnostic-tools.md)
- [Production Debugging](references/production-debug.md)
- [Compilation Issues](references/compilation.md)
- [Code Review Red Flags](references/code-review-flags.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Go, git, Delve, pprof, race-detector, linter, logging, and production diagnostic workflows.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
