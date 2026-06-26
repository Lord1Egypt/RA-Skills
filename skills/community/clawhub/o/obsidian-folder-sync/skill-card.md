## Description: <br>
Syncs Markdown files from a user-selected folder into a specified Obsidian Vault subdirectory while preserving the source folder structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soroyue](https://clawhub.ai/user/soroyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and knowledge workers use this skill to copy Markdown notes, skill files, memories, and project documentation into an Obsidian Vault for local backup or organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy private Markdown notes, agent memory, or other sensitive local content into an Obsidian Vault. <br>
Mitigation: Confirm the exact source folder, vault path, and destination subfolder before running, and avoid syncing folders that contain secrets or notes that should not be preserved in Obsidian. <br>
Risk: Running the sync creates directories and updates files under the selected vault destination. <br>
Mitigation: Use a dedicated destination subfolder and review the target path before execution so existing vault content is not unintentionally mixed with copied files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/soroyue/obsidian-folder-sync) <br>
- [Publisher profile](https://clawhub.ai/user/soroyue) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Copies only Markdown files into a user-selected Obsidian Vault subdirectory and writes a local sync log.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
