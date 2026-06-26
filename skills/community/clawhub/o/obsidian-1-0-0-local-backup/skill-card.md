## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[12357851](https://clawhub.ai/user/12357851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this skill to help an agent locate active vaults, search notes, create notes, move or rename notes, and delete notes through obsidian-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read, change, move, or delete local Obsidian notes. <br>
Mitigation: Confirm the active vault and exact note path before mutation commands, and prefer backups or version control for important vaults. <br>
Risk: Search commands may expose sensitive note contents when a task does not require them. <br>
Mitigation: Limit searches to task-relevant vaults, paths, and queries. <br>
Risk: The skill depends on an external Homebrew formula for obsidian-cli. <br>
Mitigation: Install only when the obsidian-cli Homebrew source is trusted. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [ClawHub release page](https://clawhub.ai/12357851/obsidian-1-0-0-local-backup) <br>
- [Publisher profile](https://clawhub.ai/user/12357851) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include note paths, vault names, and obsidian-cli command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
