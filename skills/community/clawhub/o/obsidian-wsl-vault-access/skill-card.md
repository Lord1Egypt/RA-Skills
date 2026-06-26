## Description: <br>
Work with an Obsidian vault stored on Windows and accessed from WSL. Read, search, create, and edit markdown notes directly through mounted paths such as /mnt/c, /mnt/d, or other /mnt/<drive> locations. Use when the user wants note operations against a Windows-hosted Obsidian vault from WSL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufei-png](https://clawhub.ai/user/wufei-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to operate on a Windows-hosted Obsidian vault from WSL. It supports reading, searching, creating, and targeted editing of markdown notes while preserving Obsidian conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read or edit more notes than intended if it is given a broad /mnt path or whole-drive root. <br>
Mitigation: Provide the exact vault root and require confirmation before broad searches, bulk edits, or important note changes. <br>
Risk: Markdown edits can break Obsidian frontmatter, wiki-links, embeds, headings, or folder conventions. <br>
Mitigation: Use targeted edits and preserve existing Obsidian structures unless the user explicitly asks to change them. <br>
Risk: Filesystem shell commands operate directly on local vault files. <br>
Mitigation: Review shell commands before execution and avoid destructive operations unless the requested file scope is clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wufei-png/obsidian-wsl-vault-access) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and filesystem paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes a user-provided vault root and WSL-mounted Windows paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
