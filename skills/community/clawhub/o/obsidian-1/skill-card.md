## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonydesign1999](https://clawhub.ai/user/tonydesign1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to work with Obsidian vaults, search note content, create notes, move or rename notes, delete notes, and directly edit Markdown files while confirming the active vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can move or delete notes in an Obsidian vault if an agent uses the wrong active vault or note path. <br>
Mitigation: Confirm the active vault and exact note path before move or delete operations, and keep backups or use an archive/trash workflow for important notes. <br>
Risk: Creating or editing notes may place content in an unintended vault when multiple vaults are configured. <br>
Mitigation: Resolve the default or open vault with obsidian-cli or Obsidian configuration before writing notes, and avoid hardcoded vault paths. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tonydesign1999/obsidian-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires obsidian-cli and an Obsidian vault; commands may operate on local note files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
