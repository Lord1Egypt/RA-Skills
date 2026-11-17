## Description:

Generate conventional commit messages by analyzing staged changes automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelatamuk](https://clawhub.ai/user/michaelatamuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze staged Git changes and draft reviewable Conventional Commits messages with appropriate type, scope, body, and footer details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commit messages may be incomplete or misleading if staged changes are broad, ambiguous, or include sensitive context.

Mitigation: Review and edit every generated message before committing.

Risk: Optional tooling setup commands can introduce supply-chain or permission risk when installed globally or run with elevated privileges.

Mitigation: Use project-local pinned dev dependencies for optional integrations and avoid elevated privileges for install commands.

## Reference(s):

- [Conventional Commits Specification](https://www.conventionalcommits.org)
- [Commit Types Quick Reference](artifact/COMMIT_TYPES_REFERENCE.md)
- [Real-World Commit Message Examples](artifact/EXAMPLES.md)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org)
- [Commitlint Documentation](https://commitlint.js.org)
- [Semantic Release Documentation](https://semantic-release.gitbook.io)
- [ClawHub Skill Page](https://clawhub.ai/michaelatamuk/skills/git-commit-message-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with Conventional Commits examples and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commit messages should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
