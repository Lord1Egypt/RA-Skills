## Description:

Use when creating slide decks, presentations, product requirement docs with diagrams, or converting markdown to PDF/PPTX/HTML slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patoo0x](https://clawhub.ai/user/patoo0x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, product teams, and other external users use this skill to create Marp slide decks and presentation-style product documents from Markdown, including diagrams, themes, exports, and common troubleshooting patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marp workflows may depend on third-party packages or remote scripts for diagram rendering.

Mitigation: Prefer pinned local dependencies and pre-render diagrams before sharing or exporting decks.

Risk: HTML rendering and local-file access can expose trusted environments to unsafe Markdown or asset paths.

Mitigation: Use --html and --allow-local-files only with trusted Markdown and trusted local assets.

## Reference(s):

- [Marp documentation](https://marp.app)
- [Marpit framework documentation](https://marpit.marp.app)
- [Marp CLI](https://github.com/marp-team/marp-cli)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, CLI commands, configuration examples, and slide templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for authoring and exporting Marp decks; it does not execute Marp by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
