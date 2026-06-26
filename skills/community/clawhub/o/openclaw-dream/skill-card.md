## Description: <br>
Automatic memory consolidation for OpenClaw agents that cleans, deduplicates, and organizes memory files such as MEMORY.md and memory/*.md when memory files accumulate noise, contradictions, stale dates, duplicates, or unmanageable size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuweifly](https://clawhub.ai/user/liuweifly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run structured memory consolidation that scans memory notes, detects stale or contradictory content, promotes durable facts, rebuilds the memory index, and writes an auditable dream log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite persistent agent memory and influence future agent behavior. <br>
Mitigation: Run it manually first, review the generated dream log and file diffs, and back up important memory files before enabling automation. <br>
Risk: Automatic cron execution can repeatedly apply memory changes without direct review. <br>
Mitigation: Enable cron only after reviewing manual runs and deciding whether daily notes should remain append-only. <br>


## Reference(s): <br>
- [OpenClaw Dream design document](references/design.md) <br>
- [OpenClaw Dream release page](https://clawhub.ai/liuweifly/openclaw-dream) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and memory-file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, generate memory/dream-log-YYYY-MM-DD.md, update memory/.last_dream, and suggest cron configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
