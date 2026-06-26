## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via notesmd-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BassShang](https://clawhub.ai/user/BassShang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to let an agent find, create, edit, move, rename, and delete notes in a local Obsidian Markdown vault through notesmd-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to read or modify local Obsidian vault files, including move, delete, and frontmatter operations. <br>
Mitigation: Review proposed file-changing commands before execution and back up important vaults before destructive or bulk operations. <br>
Risk: The skill relies on the notesmd-cli Homebrew tap and local vault discovery behavior. <br>
Mitigation: Review the Homebrew tap before installing notesmd-cli and confirm the selected vault path before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BassShang/obsidian-notesmd-cli) <br>
- [Publisher profile](https://clawhub.ai/user/BassShang) <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [Homebrew install formula: yakitrak/yakitrak/notesmd-cli](yakitrak/yakitrak/notesmd-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires notesmd-cli and access to a local Obsidian vault; commands may read and modify local Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
