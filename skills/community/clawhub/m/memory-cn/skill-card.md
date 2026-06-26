## Description: <br>
Chinese Memory Optimizer helps OpenClaw and Ollama users diagnose FTS5 Chinese tokenization issues, tune memory search settings, and maintain memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abczsl520](https://clawhub.ai/user/abczsl520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose Chinese memory-search failures, apply search and compaction configuration changes, add tags, compress logs, clean noisy memory files, and rebuild memory indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change OpenClaw memory behavior and rewrite, compress, archive, or delete memory files. <br>
Mitigation: Run diagnosis first, back up ~/.openclaw, use dry-run modes for tagging and compression, and review exact paths and configuration changes before applying them. <br>
Risk: Scheduled maintenance can repeatedly modify memory files without close review. <br>
Mitigation: Avoid cron maintenance unless backups, logs, and a rollback plan are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abczsl520/memory-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and scripts may read or modify OpenClaw memory files; review targets and use dry-run or backup options before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
