## Description:

Golang semantic code intelligence via gopls for navigating, understanding, diagnosing, formatting, and safely refactoring Go workspaces through gopls MCP tools, native LSP operations, or the gopls CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect locally resolved Go builds, find definitions and references, understand package APIs, run diagnostics, format code, and apply gopls-assisted refactors. It is intended for code that is present in the workspace and resolved through the current Go module or workspace configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local Go source files and dependencies and may contact Go module services while resolving a build.

Mitigation: Use it only in Go workspaces where this inspection is acceptable, and configure normal Go module proxy, checksum, and network controls for sensitive environments.

Risk: Refactor, format, CLI write-flag, or code-action operations can modify source files.

Mitigation: Review diffs before accepting writes, run gopls diagnostics on changed files, and run targeted Go tests for affected packages.

Risk: gopls analysis reflects the current local build configuration and may miss symbols behind other GOOS, GOARCH, or build-tag settings.

Mitigation: Re-run relevant searches, references, and diagnostics under the build tags and environment that match the code path being changed.

Risk: Call hierarchy is static and can miss calls through function values or interface dispatch.

Mitigation: Corroborate call-hierarchy results with reference searches before making changes where dynamic dispatch matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-gopls)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Source homepage](https://github.com/samber/cc-skills-golang)
- [gopls feature catalog](https://tip.golang.org/gopls/features/)
- [gopls settings reference](https://tip.golang.org/gopls/settings)
- [CLI reference](artifact/references/cli.md)
- [Feature catalog](artifact/references/features.md)
- [Capability matrix](artifact/references/matrix.md)
- [MCP and native LSP reference](artifact/references/mcp.md)
- [Settings reference](artifact/references/settings.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, tool selections, diagnostics summaries, code edits, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the local Go workspace, saved files, build tags, Go module resolution, and the selected gopls access path.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
