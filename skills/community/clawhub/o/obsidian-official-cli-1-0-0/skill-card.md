## Description: <br>
Work with Obsidian vaults through the official Obsidian CLI to open, search, create, move, edit, and manage notes, tasks, properties, links, plugins, themes, and sync operations from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justin-202603](https://clawhub.ai/user/justin-202603) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to operate Obsidian vaults through Obsidian's official CLI for note management, content search, task updates, plugin and theme administration, sync/history operations, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, edit, move, overwrite, restore, or permanently delete Obsidian vault files. <br>
Mitigation: Use explicit vault and file paths, preview planned changes, and require direct approval before overwrite, restore, or permanent delete operations. <br>
Risk: The skill can guide plugin, theme, sync, screenshot, and developer evaluation commands that may change configuration or expose sensitive workspace information. <br>
Mitigation: Approve plugin/theme installs, sync restore operations, screenshots, and eval commands only when the source and intended effect are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justin-202603/obsidian-official-cli-1-0-0) <br>
- [Obsidian Official CLI Documentation](https://help.obsidian.md/cli) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that affect vault files, plugins, themes, sync history, screenshots, and developer evaluation; user confirmation is important for destructive or sensitive operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and changelog, released 2026-02-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
