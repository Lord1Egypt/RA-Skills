## Description: <br>
Manages local Markdown note vaults from the command line, including search, note creation, moves, deletion, and basic frontmatter operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate an Obsidian-style Markdown vault from an agent session without opening a GUI. It is suited to searching notes, creating entries, editing frontmatter, moving notes with link updates, and deleting notes with review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad unrelated routing language may cause the skill to be selected for tasks outside note management. <br>
Mitigation: Restrict use to Markdown note-management requests and tighten the routing language before deployment. <br>
Risk: Commands can modify, move, or delete local Markdown files, including permanent deletion with --force. <br>
Mitigation: Use the skill only against a trusted vault, review target paths, keep backups, and avoid --force unless the target is explicitly confirmed. <br>
Risk: The skill depends on a local notes-sync CLI for filesystem operations. <br>
Mitigation: Install and invoke only a trusted notes-sync CLI and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notes-sync-cli-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, modify, move, or delete local Markdown files through the notes-sync CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
