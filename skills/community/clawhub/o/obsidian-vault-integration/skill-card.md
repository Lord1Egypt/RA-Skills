## Description: <br>
Read and write data with an Obsidian vault so agents can query notes, parse tasks and team information, and write updates back to vault files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmanock](https://clawhub.ai/user/dmanock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to an Obsidian vault used as a shared knowledge base, including reading business-plan notes, tasks, milestones, team information, and writing approved updates back to markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unchecked absolute paths or parent-directory traversal can let reads and writes escape the intended vault. <br>
Mitigation: Patch the scripts to reject absolute paths and ../ traversal, resolve target paths, and verify every resolved path stays under the configured vault root before reading or writing. <br>
Risk: Write actions can change shared vault notes and task state. <br>
Mitigation: Install only for a dedicated, backed-up vault, require explicit user approval for writes, and review the audit log for changes. <br>
Risk: Vault content may contain secrets or highly sensitive notes. <br>
Mitigation: Use a vault that excludes secrets and highly sensitive material, and review requested file paths before exposing note content to an agent. <br>


## Reference(s): <br>
- [File Format Reference](references/file-formats.md) <br>
- [ClawHub skill page](https://clawhub.ai/dmanock/obsidian-vault-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from and write to local markdown files in an Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
