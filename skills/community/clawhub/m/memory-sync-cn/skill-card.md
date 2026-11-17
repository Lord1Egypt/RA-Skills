## Description:

记忆同步系统 - 自动同步 MEMORY.md 与 CortexGraph，支持遗忘曲线和智能检索

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to synchronize MEMORY.md and daily memory logs with CortexGraph, then search, reinforce, maintain, and promote high-value memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memories, daily logs, API keys, credentials, regulated data, or client-private notes may be synced into CortexGraph.

Mitigation: Review and sanitize MEMORY.md and daily logs before syncing, and exclude secrets or sensitive records from the memory source files.

Risk: Garbage collection, consolidation, or promotion commands may alter memory stores in ways that are hard to undo.

Mitigation: Run dry-run or preview modes first, then back up CortexGraph and MEMORY.md before applying maintenance or promotion commands.

Risk: Required command-line tools may change behavior across releases.

Mitigation: Pin and verify cortexgraph and mcporter versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/memory-sync-cn)
- [Publisher Profile](https://clawhub.ai/user/guohongbin-git)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CortexGraph and mcporter command-line tools.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
