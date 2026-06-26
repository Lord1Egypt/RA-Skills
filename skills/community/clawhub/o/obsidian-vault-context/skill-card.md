## Description: <br>
Teach Claude to use an Obsidian vault as a shared workspace with persistent state across sessions, including vault navigation, orchestration file management, output routing, and bidirectional collaboration via Obsidian Headless. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tesfandiari1](https://clawhub.ai/user/tesfandiari1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Obsidian users use this skill to let an agent read and maintain vault context, create or update markdown output, and preserve task and decision state across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or edit persistent files in an Obsidian vault. <br>
Mitigation: Ask the agent to summarize intended creates, edits, or overwrites and obtain confirmation before changing important notes or operational files. <br>
Risk: Vault sync or authentication setup can expose local credentials or sensitive notes if the server is not secured. <br>
Mitigation: Keep credentials out of notes and logs, defer authentication to the user, run sync under an unprivileged account, and restrict agent work to the vault directory. <br>
Risk: Sensitive areas such as legal folders could be modified accidentally. <br>
Mitigation: Treat company/legal/ as read-only and use selective sync or workspace boundaries to limit what the agent can access. <br>


## Reference(s): <br>
- [Obsidian Headless Sync Setup](references/obsidian-headless-setup.md) <br>
- [Orchestration Files Guide](references/orchestration-files.md) <br>
- [Vault Structure Template](references/vault-structure-template.md) <br>
- [Obsidian Headless](https://obsidian.md/help/sync/headless) <br>
- [Obsidian Sync](https://obsidian.md/sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and vault file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include markdown files, status updates, task lists, decision logs, and Obsidian wikilinks within the configured vault.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
