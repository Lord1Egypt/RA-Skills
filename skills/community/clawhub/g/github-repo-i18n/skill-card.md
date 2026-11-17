## Description:

Internationalize the user-facing language layer of a GitHub repository, including its repository description, repository topics, README files, release notes, changelogs, and other explicitly selected documentation, with English as the default and any user-requested locales as mirrors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers and maintainers use this skill to localize GitHub repository documentation and selected repository metadata while preserving project facts, links, commands, code blocks, and cross-locale structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect and edit selected repository documentation for localization.

Mitigation: Confirm the exact files, documentation surfaces, and target locales before allowing edits.

Risk: Localized documentation or metadata drafts could change project meaning or create misleading repository-facing text.

Mitigation: Review the final document diff, locale matrix, GitHub-style previews, and semantic translation quality before accepting changes.

Risk: Repository description or topic updates affect remote GitHub metadata when explicitly authorized.

Mitigation: Review the final description and topic list before authorizing any remote metadata write.

## Reference(s):

- [Document parity](references/document-parity.md)
- [GitHub repository metadata](references/github-repository-metadata.md)
- [Locale strategy](references/locale-strategy.md)
- [Preview and GitHub rendering](references/preview-and-github-rendering.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, metadata drafts, audit commands, audit reports, and concise review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local documentation edits and offline audit output; semantic translation quality requires human review.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
