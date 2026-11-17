## Description:

Comprehensive documentation guide for Golang projects, covering godoc comments, README, CONTRIBUTING, CHANGELOG, Go Playground, Example tests, API docs, and llms.txt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write and review Go project documentation, including godoc comments, README, CONTRIBUTING, CHANGELOG, examples, API documentation, and AI-facing documentation files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit documentation and Go files, so generated changes may introduce inaccurate or misleading project guidance.

Mitigation: Review proposed documentation and code changes before merging, with special attention to factual claims, obligations, examples, and generated configuration.

Risk: The skill requests broad Git and network authority for documentation work.

Mitigation: Review Git operations before allowing remote, history-changing, config-changing, reset, clean, checkout, or push actions, and approve web fetches only when they are needed for the documentation task.

Risk: Generated Docker instructions may use floating image tags.

Mitigation: Prefer pinned image versions over latest-style tags in generated Docker commands and documentation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-documentation)
- [Project Homepage](https://github.com/samber/cc-skills-golang)
- [Application Documentation](artifact/references/application.md)
- [Code Comments](artifact/references/code-comments.md)
- [Library Documentation](artifact/references/library.md)
- [Project Documentation](artifact/references/project-docs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and code snippets with optional shell commands and file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce documentation files, Go examples, project documentation guidance, and review findings.]

## Skill Version(s):

1.2.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
