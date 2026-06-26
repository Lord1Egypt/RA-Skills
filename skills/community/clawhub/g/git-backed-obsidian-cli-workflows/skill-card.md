## Description: <br>
Use the official Obsidian CLI for note workflows in a Git-backed vault, including search, read, links/backlinks-style queries, daily-note operations, and lightweight note writes that auto-sync after successful write operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarinRowe](https://clawhub.ai/user/DarinRowe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-taking power users use this skill to query and update an Obsidian vault through the official CLI while keeping successful writes synchronized to Git. It is intended for environments where the Obsidian CLI is already installed and working. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic Git commits and pushes can publish unintended vault contents to the configured remote. <br>
Mitigation: Use a dedicated vault repository, verify the remote and branch, keep secrets out of the vault, and review changes before enabling automated sync. <br>
Risk: Fallback write paths or note names could modify files outside the intended vault if paths are not constrained. <br>
Mitigation: Avoid absolute paths and parent-directory segments in note targets, and prefer the official CLI path when it supports the requested workflow. <br>
Risk: The backup script path is configurable and can execute trusted local code after write workflows. <br>
Mitigation: Treat NOTES_BACKUP_SCRIPT as trusted code execution and point it only to reviewed backup scripts. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/DarinRowe/git-backed-obsidian-cli-workflows) <br>
- [Environment note](references/environment-note.md) <br>
- [Fallback policy](references/fallbacks.md) <br>
- [Query vs write](references/query-vs-write.md) <br>
- [Workflow surface](references/workflow-surface.md) <br>
- [obsidian-official-cli-headless companion skill](https://clawhub.ai/DarinRowe/obsidian-official-cli-headless) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operation status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the workflow used, target note or path, whether sync ran, and whether sync succeeded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
