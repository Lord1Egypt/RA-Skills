## Description:

Guides agents through setting up markdownlint-cli2 and pre-commit checks, repairing common Markdown lint violations, and removing horizontal rules while preserving YAML frontmatter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Markdown formatting checks, pre-commit hooks, repository-wide lint repair commands, and horizontal-rule validation to documentation repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-wide lint fixes and horizontal-rule cleanup can modify many Markdown files.

Mitigation: Run bulk --fix and cleanup commands only in a clean git working tree, preview affected files where possible, and review diffs before committing.

Risk: Unpinned markdownlint-cli2 or hook versions can change lint behavior over time.

Mitigation: Prefer a pinned markdownlint-cli2 version or project devDependency with a committed lockfile before installing or running hooks.

## Reference(s):

- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- [Node.js](https://nodejs.org/)
- [ClawHub skill page](https://clawhub.ai/niracler/skills/nini-markdown-lint)
- [Horizontal rule checker script](artifact/scripts/check-horizontal-rules.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON, YAML, Bash, and text code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository-wide lint and fix commands that modify Markdown files.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
