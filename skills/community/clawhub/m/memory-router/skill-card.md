## Description: <br>
Memory Router helps OpenClaw agents manage local memory by tiering bloated MEMORY.md files, generating query-aware manifests, auditing duplicate or conflicting memories, and maintaining session state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlacroix82](https://clawhub.ai/user/jlacroix82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep long-running OpenClaw memory stores concise, searchable, and relevant across sessions. It is intended for local workflows that need memory manifests, audits, entity indexing, and controlled MEMORY.md tiering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and modifies local memory files as part of its normal purpose. <br>
Mitigation: Install only for workflows that intentionally delegate local memory-file management, and keep separate backups of MEMORY.md and memory/ before write operations. <br>
Risk: Tiering and restore operations can rewrite or overwrite MEMORY.md. <br>
Mitigation: Run --tier --dry-run first, review the proposed changes, then use --tier --confirm only when ready; do not place --tier --confirm or --restore --force in unattended automation. <br>
Risk: Archive retention settings can lead to irreversible deletion of archived memory sections. <br>
Mitigation: Use conservative retention settings, back up the full memory directory, and monitor archived files before reducing retention periods. <br>
Risk: Persistent helper commands such as entity updates and WAL updates write local state files. <br>
Mitigation: Review these commands before automating them, and reserve unattended runs for commands documented as safe such as --compact, --audit, --status, entity list/search, WAL get, and --tier --dry-run. <br>


## Reference(s): <br>
- [Memory Router on ClawHub](https://clawhub.ai/jlacroix82/memory-router) <br>
- [README.md](artifact/README.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON manifests, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local files such as memory/memory-manifest.json, memory/memory-audit-report.md, entity indexes, session state, backups, archives, and updated MEMORY.md content depending on the command used.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
