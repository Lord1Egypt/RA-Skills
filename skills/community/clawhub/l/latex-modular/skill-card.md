## Description:

LaTeX Modular helps agents extract, compose, refactor, inject, convert, and validate modular LaTeX document components using bundled Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and document authors use this skill to build or restructure LaTeX documents from reusable components and validate generated documents with local LaTeX tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local LaTeX compilers and modify or delete local files.

Mitigation: Run it only in a sandboxed or disposable workspace, use trusted LaTeX sources, and review proposed file operations before execution.

Risk: Custom engine values or arbitrary file paths can expand the scope of local execution and file writes.

Mitigation: Keep engine choices to expected LaTeX binaries, pass scoped workspace paths, and avoid allowing arbitrary path or engine arguments.

## Reference(s):

- [Usage Guide](references/guide.md)
- [Architecture](references/architecture.md)
- [Component Specification](references/component-spec.md)
- [Permissions](references/permissions.md)
- [Antipatterns](references/antipatterns.md)
- [FAQ](references/faq.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples plus generated LaTeX source, validation reports, and configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local Python and LaTeX tools and may write generated .tex, PDF, component, manifest, and report files.]

## Skill Version(s):

1.3.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
