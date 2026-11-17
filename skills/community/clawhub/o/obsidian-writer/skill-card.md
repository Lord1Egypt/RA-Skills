## Description:

Write Obsidian-compatible .md notes and .canvas files for vault sync via Git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hekate2639](https://clawhub.ai/user/hekate2639)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge workers use this skill to create Obsidian vault notes, daily logs, project docs, and JSON Canvas diagrams with Obsidian-specific syntax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write files into an Obsidian vault, which may alter notes or canvas diagrams.

Mitigation: Confirm the vault path before use and review generated Markdown and canvas JSON before relying on it.

Risk: The workflow can commit and push vault changes to a Git remote.

Mitigation: Confirm the Git remote and require explicit approval before any push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hekate2639/skills/obsidian-writer)
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub repository](https://github.com/obsidianmd/jsoncanvas)
- [Obsidian supported file formats](https://help.obsidian.md/file-formats)
- [Canvas reference](references/canvas-spec.md)
- [File formats reference](references/file-formats.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Obsidian Markdown notes and JSON Canvas files, with optional Git command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs target a user-selected Obsidian vault and use UTF-8 text files with vault-relative attachment paths.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
