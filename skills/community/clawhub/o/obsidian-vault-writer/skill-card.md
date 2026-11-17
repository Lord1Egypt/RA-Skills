## Description:

Saves content to an Obsidian vault, appends to daily notes, and writes structured agent output into vault notes in VPS and headless server environments using notesmd-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to save agent-generated Markdown, summaries, drafts, and structured notes into an accessible Obsidian vault, including daily notes and named note files. It is designed for headless, VPS, server, and CI environments where the Obsidian desktop app is not running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies an Obsidian vault, so incorrect target selection or generated content could change user notes unexpectedly.

Mitigation: Confirm the vault once per session, keep vault backups or version control, and require explicit user consent before overwriting existing notes.

Risk: The security summary identifies unsafe command templates for note content.

Mitigation: Invoke notesmd-cli without shell string interpolation for user-supplied content, and review generated commands before execution.

Risk: The security summary identifies reliance on an unpinned third-party CLI install.

Mitigation: Install notesmd-cli only from a trusted source, prefer a pinned and verified version in a user-owned path, and re-check the CLI version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/obsidian-vault-writer)
- [notesmd-cli Reference](references/notesmd-cli.md)
- [Obsidian Flavored Markdown Reference](references/obsidian-markdown.md)
- [Obsidian Canvas (JSON Canvas) Reference](references/obsidian-canvas.md)
- [Obsidian Bases Reference](references/obsidian-bases.md)
- [notesmd-cli source](https://github.com/Yakitrak/notesmd-cli)
- [Obsidian Bases syntax](https://help.obsidian.md/bases/syntax)
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [Obsidian Flavored Markdown docs](https://help.obsidian.md/obsidian-flavored-markdown)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Obsidian note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, append, or overwrite vault notes through notesmd-cli after vault confirmation and user consent for overwrites.]

## Skill Version(s):

0.2.1 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
