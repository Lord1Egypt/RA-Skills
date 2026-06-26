## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to locate Obsidian vaults, search notes, and create, move, rename, or delete Markdown notes through obsidian-cli while respecting vault conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, move, rename, or delete local Markdown notes in selected Obsidian vaults. <br>
Mitigation: Require user confirmation before write operations and review target vault paths before running obsidian-cli commands. <br>
Risk: The skill depends on an external obsidian-cli Homebrew formula. <br>
Mitigation: Verify the Homebrew source before installation and confirm that obsidian-cli is the intended binary. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nidhov01/nidhov01-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local Obsidian vault paths and obsidian-cli commands when the user directs note operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
