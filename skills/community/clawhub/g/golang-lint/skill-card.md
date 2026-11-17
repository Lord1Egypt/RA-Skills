## Description:

Linting best practices and golangci-lint configuration for Go projects, including running linters, configuring .golangci.yml, suppressing warnings with nolint directives, interpreting lint output, and selecting linters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up golangci-lint, interpret and fix lint findings, write disciplined nolint suppressions, and adopt linting workflows in Go codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing golangci-lint with an unpinned latest version can change lint behavior over time.

Mitigation: Pin and review the golangci-lint version used by local setup and CI.

Risk: Auto-fix commands can modify Go code in ways that still need developer review.

Mitigation: Review diffs and run the relevant test suite before accepting --fix output.

Risk: Using the skill outside Go linting work may produce irrelevant guidance.

Mitigation: Invoke it for Go linting, golangci-lint configuration, lint-output interpretation, or nolint guidance.

## Reference(s):

- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Linter Reference](references/linter-reference.md)
- [Nolint Directives](references/nolint-directives.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Go, YAML, Makefile, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose golangci-lint commands, .golangci.yml changes, nolint directives, and cleanup plans for Go files.]

## Skill Version(s):

1.4.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
