## Description: <br>
A command-line skill for searching, analyzing, exporting, and batch-processing notes in a local Obsidian vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Obsidian users and agents use this skill to inspect local vaults, search note content, generate vault statistics, export notes, and manage links or tags from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk replace operations can rewrite many private notes without preview, confirmation, backup, or rollback safeguards. <br>
Mitigation: Prefer read-only commands first, back up the vault, and require explicit user approval before replace or other broad write operations. <br>
Risk: Local Obsidian vaults may contain private or sensitive notes that can be searched, summarized, exported, or copied to another directory. <br>
Mitigation: Confirm the vault and output paths before running commands, and limit exports to the minimum needed note set. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/obsidian-cli-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and command-line text or exported note files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on a local Obsidian vault path and may write modified notes or exported files when write-capable commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
