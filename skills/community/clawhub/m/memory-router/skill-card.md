## Description:

Memory Router helps agents manage local memory files by generating focused manifests, tiering oversized MEMORY.md content, auditing duplicate or conflicting entries, and maintaining entity and session-state indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memory Router to reduce memory context bloat, route only relevant memory files into a session, and inspect local memory health before loading or rewriting memory state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tiering, restore, cleanup, entity, and WAL commands can modify or overwrite local memory files.

Mitigation: Use a backed-up workspace, run status or dry-run commands first, and reserve --tier --confirm and --restore --force for reviewed manual execution.

Risk: Custom workspace or path settings can increase the chance of operating on the wrong files.

Mitigation: Avoid absolute paths or .. components in custom path settings and confirm the workspace before running commands that write files.

Risk: The security verdict is suspicious because destructive restore and tiering guarantees may be weaker than the documentation suggests.

Mitigation: Treat the skill as an assisted local memory tool, review generated manifests and audit reports, and do not rely on its backups as the only recovery mechanism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/memory-router)
- [README](artifact/README.md)
- [Installation Guide](artifact/INSTALL.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, generated JSON manifests, text status output, and Markdown audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local filesystem outputs may include memory/memory-manifest.json, memory/memory-audit-report.md, archive files, backups, entity indexes, and SESSION-STATE.md depending on the command.]

## Skill Version(s):

2.4.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
