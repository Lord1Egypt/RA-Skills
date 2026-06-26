## Description: <br>
Persistent memory system for OpenClaw agents that reads session logs, extracts facts, decisions, and solutions, manages a temperature-based lifecycle, and generates MEMORY_SNAPSHOT.md for agent context injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blusehuang1121](https://clawhub.ai/user/blusehuang1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain durable agent memory across sessions, consolidate high-signal facts and decisions, and inject a compact memory snapshot into future agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory text may be sent to a remote LLM provider during semantic consolidation. <br>
Mitigation: Confirm provider settings and the exact memory content sent off-device before enabling; disable or restrict the semantic step if remote processing is not acceptable. <br>
Risk: The skill can persist user profile data, snapshots, archives, and memory-derived traits. <br>
Mitigation: Define retention and deletion practices before use, and periodically review stored memory files for sensitive or stale content. <br>
Risk: Cron jobs and agent context hooks can run consolidation automatically and alter future agent behavior. <br>
Mitigation: Review cron schedules and hook configuration before installation, test manually first, and keep a rollback path for disabling automatic injection. <br>


## Reference(s): <br>
- [Memory Consolidate README](scripts/memory_consolidate/README.md) <br>
- [Memory Consolidate on ClawHub](https://clawhub.ai/blusehuang1121/memory-consolidate) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown snapshot files, JSON or JSONL memory state, shell commands, and terminal health reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update workspace memory files, cron jobs, and agent context hooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
