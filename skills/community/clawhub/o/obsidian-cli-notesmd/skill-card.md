## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Michael-C-Matias](https://clawhub.ai/user/Michael-C-Matias) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to locate active Obsidian vaults, search notes, create notes, move or rename notes while preserving links, and delete notes through obsidian-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can modify local Obsidian vault content, including creating, moving, renaming, or deleting notes. <br>
Mitigation: Review proposed obsidian-cli commands before execution and prefer link-aware move operations when refactoring notes. <br>
Risk: Using the wrong vault can affect personal or work notes in an unintended location. <br>
Mitigation: Resolve the active or default vault with obsidian-cli or Obsidian's vault configuration before running write operations. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Michael-C-Matias/obsidian-cli-notesmd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires obsidian-cli and, for note creation with --open, a working Obsidian URI handler.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
