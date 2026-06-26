## Description: <br>
Official Obsidian CLI (v1.12+) provides a complete command-line interface for Obsidian notes, tasks, search, tags, properties, links, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexanderkinging](https://clawhub.ai/user/alexanderkinging) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to let an AI assistant operate an Obsidian vault through the official CLI for note creation, reading, search, task management, metadata, links, publishing, plugins, themes, and workspace commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI assistant broad ability to read, change, delete, publish, customize, and run code in an Obsidian vault. <br>
Mitigation: Install only when that level of vault access is intended, limit use to trusted vaults, and require explicit confirmation before delete, restore, publish, plugin install or enable, theme/workspace changes, bulk edits, eval, or developer commands. <br>
Risk: Vault edits and destructive commands can cause data loss or unwanted publication. <br>
Mitigation: Keep backups or version history enabled and review assistant-proposed changes before execution. <br>
Risk: Server-resolved GitHub import provenance is unavailable for this release. <br>
Mitigation: Use the ClawHub release as the distribution record and verify any optional Homebrew or GitHub source before installing outside ClawHub. <br>


## Reference(s): <br>
- [Official Obsidian CLI documentation](https://help.obsidian.md/cli) <br>
- [ClawHub skill page](https://clawhub.ai/alexanderkinging/obsidian-cli-official) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference material with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Obsidian 1.12+ with the CLI enabled and Obsidian running; publish commands require an Obsidian Publish subscription.] <br>

## Skill Version(s): <br>
4.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
