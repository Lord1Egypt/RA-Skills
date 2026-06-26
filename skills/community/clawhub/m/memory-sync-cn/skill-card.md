## Description: <br>
记忆同步系统 - 自动同步 MEMORY.md 与 CortexGraph，支持遗忘曲线和智能检索 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to synchronize OpenClaw MEMORY.md and daily memory logs into CortexGraph, then retrieve, reinforce, consolidate, and promote high-value memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy sensitive MEMORY.md and daily-log content, including API keys, tokens, passwords, account details, or other secrets, into a persistent searchable memory backend. <br>
Mitigation: Remove secrets and sensitive account details before syncing; use dry-run or preview modes first; keep backups before running garbage collection or consolidation. <br>
Risk: Memory maintenance operations can promote, consolidate, or delete stored memories in ways that affect future recall. <br>
Mitigation: Review promoted memory candidates manually, prefer preview and dry-run modes, and run destructive maintenance only after confirming the stored content is appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/memory-sync-cn) <br>
- [Publisher profile](https://clawhub.ai/user/guohongbin-git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cortexgraph and mcporter command-line tools; sync scripts support dry-run or preview modes for selected operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
