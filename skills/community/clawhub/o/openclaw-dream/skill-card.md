## Description:

Automatic memory consolidation for OpenClaw agents that cleans, deduplicates, and organizes MEMORY.md, daily memory notes, and self-improving logs when memory has accumulated noise, contradictions, stale dates, duplicates, or excessive size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuweifly](https://clawhub.ai/user/liuweifly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to consolidate persistent agent memory, resolve stale or duplicate memory entries, promote important daily notes into long-term memory, rebuild the memory index, and produce an audit-friendly dream log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change long-term agent memory and memory index state.

Mitigation: Disable cron or heartbeat triggers until backups and a dry-run or diff review process are in place.

Risk: Broad manual and automatic triggers can start memory consolidation when the user did not intend persistent memory edits.

Mitigation: Use narrower explicit triggers and require review before applying memory changes.

Risk: Weak concurrency safeguards can allow overlapping consolidation runs to compete over memory files.

Mitigation: Use a real lock around the full consolidation run and verify stale locks before removing them.

## Reference(s):

- [OpenClaw Dream design reference](references/design.md)
- [OpenClaw Dream ClawHub page](https://clawhub.ai/liuweifly/skills/openclaw-dream)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated memory log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md, memory/.last_dream, memory/self-improving/.last_distill, the memory vector index, and memory/dream-log-YYYY-MM-DD.md during use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
