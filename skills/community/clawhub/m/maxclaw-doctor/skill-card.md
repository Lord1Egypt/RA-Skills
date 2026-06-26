## Description: <br>
Helps OpenClaw users protect files by recording file-operation versions and supporting delete recovery and modification rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OreoAndYuumi](https://clawhub.ai/user/OreoAndYuumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create local records before file modifications or deletions, then recover deleted files or roll back tracked edits when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain local copies of files it records or deletes, including sensitive files if used on secrets or personal documents. <br>
Mitigation: Limit use to intended project files, avoid secrets and personal documents, and review access to ~/.openclaw/minivcs/. <br>
Risk: Cleanup, remove, restore, and rollback operations can delete retained records or overwrite current file contents. <br>
Mitigation: Require explicit user confirmation, show the target path and record ID, and review current file state before running destructive or overwriting commands. <br>
Risk: The skill can operate outside a project boundary if given broad paths. <br>
Mitigation: Keep the project root scoped to the intended workspace and avoid running file-protection commands against system, home-directory, or unrelated paths. <br>


## Reference(s): <br>
- [Python downloads for macOS](https://www.python.org/downloads/macos/) <br>
- [Python downloads for Windows](https://www.python.org/downloads/windows/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, record IDs, retention periods, and recovery or rollback commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
