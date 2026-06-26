## Description: <br>
Autonomous memory consolidation for OpenClaw agents that periodically gathers signal from daily logs, session transcripts, learnings, and plans; consolidates durable knowledge into MEMORY.md; optionally syncs structured knowledge to an Obsidian vault; and prunes stale or contradictory entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oryanmoshe](https://clawhub.ai/user/oryanmoshe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep long-running agent memory coherent by consolidating daily logs, learnings, session-transcript matches, and active plans into durable memory. It is also used to configure an optional Obsidian knowledge-base sync for people, projects, plans, tools, and decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private memory logs, learnings, plan files, and matched session transcript lines. <br>
Mitigation: Use it only in workspaces where those sources are appropriate for autonomous review, and add redaction or approval controls before using it around secrets or sensitive client data. <br>
Risk: The skill can silently rewrite durable memory and mark learning entries as promoted. <br>
Mitigation: Review MEMORY.md, learning-file diffs, and memory/dreaming-log.md regularly after dream cycles. <br>
Risk: Optional Obsidian sync can export consolidated memory into an external vault. <br>
Mitigation: Keep Obsidian sync disabled unless the configured vault is approved for the information being consolidated. <br>


## Reference(s): <br>
- [Memory Dreaming Skill](https://clawhub.ai/oryanmoshe/memory-dreaming) <br>
- [Architecture - Memory Dreaming](references/architecture.md) <br>
- [Dream Prompt](references/dream-prompt.md) <br>
- [Obsidian Sync - How It Works](references/obsidian-sync.md) <br>
- [Dreaming Configuration Defaults](assets/dreaming-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify MEMORY.md, memory/dreaming-log.md, learning status files, and optional Obsidian Markdown notes when executed by an agent.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
