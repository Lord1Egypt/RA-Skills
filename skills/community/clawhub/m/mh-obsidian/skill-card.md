## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to locate Obsidian vaults, search Markdown notes, and manage notes with obsidian-cli commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent read, create, move, rename, or delete notes in an Obsidian vault. <br>
Mitigation: Keep backups or Obsidian sync/version history enabled, and approve commands only for vaults and files you intend to manage. <br>
Risk: Commands may target the wrong vault if the active or default Obsidian vault is misunderstood. <br>
Mitigation: Verify the vault with obsidian-cli print-default --path-only or the Obsidian desktop vault configuration before running mutation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-obsidian) <br>
- [Obsidian Help](https://help.obsidian.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and note-management guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires obsidian-cli and an accessible Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
