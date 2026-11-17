## Description:

OpenClaw + Ollama 中文记忆系统优化。诊断 FTS5 unicode61 中文分词 bug，优化搜索参数，自动维护记忆文件。命中率从 55% 提升到 100%。

This skill is ready for commercial/non-commercial use.

## Publisher:

[abczsl520](https://clawhub.ai/user/abczsl520)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to diagnose Chinese memory-search issues, tune memory search settings, add tags, compress old logs, clean noisy memory files, and rebuild memory indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite, compress, delete, and reconfigure persistent OpenClaw memory files.

Mitigation: Run dry-run modes first, create independent backups of memory directories, and inspect results before relying on modified or archived logs.

Risk: Memory directories writable by other users could expose maintenance scripts to untrusted files.

Mitigation: Run the skill only on memory directories with trusted ownership and permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abczsl520/skills/memory-cn)
- [Publisher profile](https://clawhub.ai/user/abczsl520)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnostic recommendations and may run scripts that inspect, rewrite, compress, delete, or reindex persistent OpenClaw memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
