## Description:

Golang Pkg Go Dev helps agents look up Go package and module documentation, symbols, examples, versions, importers, licenses, and known vulnerabilities through the read-only godig pkg.go.dev client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to retrieve Go package documentation, exported APIs, examples, dependency metadata, available versions, importers, licenses, and vulnerability information while answering Go library questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broader local edit, git, Go, and agent permissions than its read-only package lookup purpose requires.

Mitigation: Review permissions before installing and narrow execution to godig-only access when the harness supports tool scoping.

Risk: Installing godig with an unpinned latest version can change behavior after review.

Mitigation: Pin godig to a reviewed version for controlled environments.

Risk: Using the public hosted MCP endpoint can expose sensitive or private package lookup queries to an external service.

Mitigation: Use a local godig CLI or self-hosted MCP server for private codebase or sensitive dependency investigations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-pkg-go-dev)
- [cc-skills-golang repository](https://github.com/samber/cc-skills-golang)
- [pkg.go.dev](https://pkg.go.dev)
- [sample-output.md](references/sample-output.md)
- [godig hosted MCP endpoint](https://godig.samber.dev/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pkg.go.dev-derived package metadata, API references, examples, version lists, importer lists, licenses, and vulnerability summaries.]

## Skill Version(s):

1.4.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
