## Description: <br>
Helps an agent use notesmd-cli to search, create, edit, move, delete, and manage frontmatter in an Obsidian vault without running Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kxindot](https://clawhub.ai/user/kxindot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to manage Obsidian vault content from Linux, WSL2, headless, or terminal-first environments. It supports vault setup, note search, note creation and editing, moves, deletion, daily notes, and frontmatter updates through notesmd-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Note-editing, overwrite, move, and delete operations can change or remove Obsidian vault content. <br>
Mitigation: Confirm the exact target notes before executing destructive or overwriting actions, and keep a backup or version control enabled for the vault. <br>
Risk: Direct filesystem renames or moves may not update Obsidian wikilinks. <br>
Mitigation: Use notesmd-cli move when renaming or moving notes that may be linked from other vault files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kxindot/obsidian-wsl) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kxindot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose note edits, moves, deletes, overwrites, or direct filesystem operations against Obsidian vault files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
