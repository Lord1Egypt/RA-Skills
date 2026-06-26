## Description: <br>
Provides an agent-facing reference for the official Obsidian CLI (v1.12+) to automate vault files, daily notes, search, tasks, metadata, links, themes, plugins, sync, publish, workspaces, and developer tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adolago](https://clawhub.ai/user/adolago) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Obsidian users use this skill to ask an agent for Obsidian CLI commands that inspect, modify, organize, publish, and troubleshoot vault content. It is suited to environments where the user intends to let an agent operate a running Obsidian instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault-changing commands can delete, overwrite, restore, publish, or otherwise modify Obsidian vault content. <br>
Mitigation: Require explicit approval for destructive or publishing actions, operate only on trusted vaults, and keep backups or version history available. <br>
Risk: Plugin and theme commands can install, enable, disable, or remove third-party code and change restricted-mode posture. <br>
Mitigation: Require approval for plugin, theme, and restricted-mode changes, and verify community packages before use. <br>
Risk: Developer commands can run JavaScript, inspect DOM or CSS, use Chrome DevTools Protocol, and access console or debug data in Obsidian. <br>
Mitigation: Keep CLI and debug capabilities enabled only where needed, verify the Obsidian binary is official, and require approval for eval, CDP, DOM, console, debug, and screenshot actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require a running Obsidian 1.12+ instance with CLI enabled.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
