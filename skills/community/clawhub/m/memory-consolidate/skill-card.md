## Description:

Persistent memory system for OpenClaw agents that reads session logs, extracts facts, decisions, and solutions, manages temperature-based lifecycle, and generates MEMORY_SNAPSHOT.md for session context injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blusehuang1121](https://clawhub.ai/user/blusehuang1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to consolidate agent session memory into structured facts, events, summaries, health metrics, and a compact snapshot that can be injected into future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected persistent memory content to a configured LLM endpoint for semantic consolidation.

Mitigation: Use only a trusted HTTPS endpoint with a dedicated low-privilege API key, and disable the semantic step for workspaces containing secrets or sensitive client data.

Risk: Generated MEMORY_SNAPSHOT.md content can be injected into future agent sessions and may influence later behavior.

Mitigation: Review generated snapshots before enabling session injection, especially after first install or configuration changes.

Risk: Daily cron can automate ongoing memory collection and persistence.

Mitigation: Enable the cron job only when persistent scheduled consolidation is intended, and confirm the workspace scope before running it.

## Reference(s):

- [Memory Consolidate ClawHub Page](https://clawhub.ai/blusehuang1121/skills/memory-consolidate)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/scripts/memory_consolidate/README.md](artifact/scripts/memory_consolidate/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown snapshots, JSON/JSONL memory records, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent workspace memory files and health reports; optional semantic consolidation may use a configured LLM provider.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
