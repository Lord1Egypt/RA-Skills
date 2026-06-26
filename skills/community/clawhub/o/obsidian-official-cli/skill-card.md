## Description: <br>
Work with Obsidian vaults using the official Obsidian CLI (v1.12+). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slmoloch](https://clawhub.ai/user/slmoloch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to manage Obsidian vaults from the terminal, including note operations, search, tasks, properties, links, plugins, themes, sync, and developer-oriented Obsidian CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad ability to change, delete, restore, install, sync, and run code inside an Obsidian vault. <br>
Mitigation: Require explicit confirmation for delete, permanent delete, overwrite, move, restore, plugin or theme changes, sync changes, and any obsidian eval command. <br>
Risk: Commands may affect important or sensitive Obsidian vault content. <br>
Mitigation: Prefer testing on a backed-up or non-sensitive vault before using the skill on important notes. <br>


## Reference(s): <br>
- [Obsidian Official CLI Documentation](https://help.obsidian.md/cli) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/slmoloch/obsidian-official-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Obsidian CLI commands that create, modify, delete, restore, install, sync, or evaluate content in an Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-02-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
