## Description: <br>
Use when saving content to an Obsidian vault, appending to daily notes, or writing structured output from another skill into a vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to save generated Markdown, summaries, drafts, and structured notes into an accessible Obsidian vault without requiring the Obsidian desktop app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes to local Obsidian vault files through a third-party CLI. <br>
Mitigation: Confirm the notesmd-cli package is trusted and verify the selected vault path before allowing the agent to write. <br>
Risk: Overwrite, move, or delete operations can change or remove existing notes. <br>
Mitigation: Require explicit user confirmation before overwrite, move, or delete actions. <br>
Risk: Vault credentials or sync tokens could be exposed if included in notes or chat context. <br>
Mitigation: Do not store vault credentials or sync tokens in notes or conversation context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/obsidian-vault-writer) <br>
- [notesmd-cli reference](references/notesmd-cli.md) <br>
- [notesmd-cli source](https://github.com/Yakitrak/notesmd-cli) <br>
- [Obsidian Flavored Markdown reference](references/obsidian-markdown.md) <br>
- [Obsidian Canvas reference](references/obsidian-canvas.md) <br>
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/) <br>
- [Obsidian Bases reference](references/obsidian-bases.md) <br>
- [Obsidian Bases syntax](https://help.obsidian.md/bases/syntax) <br>
- [Obsidian Flavored Markdown docs](https://help.obsidian.md/obsidian-flavored-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and Obsidian note content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose notesmd-cli commands that append, create, overwrite, move, or delete notes after user confirmation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
