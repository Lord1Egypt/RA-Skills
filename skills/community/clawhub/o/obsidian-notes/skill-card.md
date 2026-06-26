## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[164149043](https://clawhub.ai/user/164149043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to help an agent find, create, edit, move, or delete Markdown notes in a local Obsidian vault through obsidian-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to delete or move local notes, which may remove or reorganize important vault content. <br>
Mitigation: Verify the active vault and exact note path before destructive commands; prefer backups or non-destructive archive moves for important notes. <br>
Risk: The skill depends on obsidian-cli and the local Obsidian URI handler, so commands may fail or target the wrong vault if local configuration is stale. <br>
Mitigation: Confirm obsidian-cli installation, the default vault, and the active Obsidian vault before making changes. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/164149043/obsidian-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local vault paths and note names supplied by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
