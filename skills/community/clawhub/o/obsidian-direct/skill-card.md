## Description: <br>
Work with Obsidian vaults as a knowledge base by searching notes, creating and editing Markdown notes with frontmatter, and managing tags and wikilinks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RuslanLanket](https://clawhub.ai/user/RuslanLanket) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, read, create, and update notes in an Obsidian Markdown vault. It is suited for knowledge-base queries, saving new notes, organizing notes, and prompt-driven edits to existing notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and overwrite local Obsidian notes. <br>
Mitigation: Install it only for vaults the agent should access, keep backups or version history enabled, and require confirmation or diff review before replace, clear, or overwrite operations. <br>
Risk: The artifact includes a hardcoded default vault path. <br>
Mitigation: Set OBSIDIAN_VAULT or pass --vault to the intended vault before use. <br>
Risk: Vault notes may contain sensitive information that search or read commands can expose to the agent. <br>
Mitigation: Avoid storing secrets in the vault and review retrieved note content before using it in external outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RuslanLanket/obsidian-direct) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, read, and modify Markdown files in a configured Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
