## Description:

Guides agents building Go services with samber/hot in-memory caches, including eviction selection, TTLs, loaders, sharding, stale-while-revalidate, missing-key caching, and Prometheus metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adopting or maintaining samber/hot caches in Go codebases, especially to choose algorithms, size capacity, add loaders and TTL behavior, and avoid common runtime mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command uses an unpinned Go dependency update, which can pull a newer release than intended.

Mitigation: Prefer a pinned command such as go get github.com/samber/hot@vX.Y.Z, then review go.mod and go.sum changes and run normal Go dependency checks.

Risk: Cache configuration mistakes can produce stale data, loader-error blind spots, excessive memory use, or runtime panics from incompatible options.

Mitigation: Use TTLs with janitor cleanup, check loader errors, size caches from measured item cost and memory budget, and avoid mutually exclusive options such as WithoutLocking with WithJanitor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-samber-hot)
- [cc-skills-golang repository](https://github.com/samber/cc-skills-golang)
- [samber/hot package documentation](https://pkg.go.dev/github.com/samber/hot)
- [samber/hot repository](https://github.com/samber/hot)
- [Algorithm Selection Guide](references/algorithm-guide.md)
- [API Reference](references/api-reference.md)
- [Production Patterns](references/production-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Go code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Go tooling for install and verification commands.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
