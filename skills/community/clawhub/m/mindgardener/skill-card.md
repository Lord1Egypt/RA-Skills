## Description:

Local-first long-term memory for autonomous agents. Built for OpenClaw. Creates wiki knowledge graph from conversations, scores events by surprise, detects conflicts, and assembles token-budget context. Complements OpenClaw's built-in memory_search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[widingmarcus-cyber](https://clawhub.ai/user/widingmarcus-cyber)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use MindGardener to build and retrieve persistent memory from conversation logs, including entity wiki pages, graph relationships, surprise scoring, conflict checks, and token-budget recall context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private agent logs may be sent to remote LLM providers during extraction or related memory maintenance.

Mitigation: Choose and verify the intended local or remote provider before use, and avoid processing private logs until the configured extraction path is confirmed.

Risk: Generated MEMORY.md and RECALL-CONTEXT.md can expose sensitive, stale, or incorrect memory to downstream agents.

Mitigation: Inspect generated memory and recall context before loading them into agent sessions, especially in workspaces containing private logs.

Risk: Scheduled maintenance and apply-style commands can change, consolidate, or prune memory files without a manual review step.

Mitigation: Enable cron or apply-style maintenance only after backups, retention rules, and review procedures are in place.

## Reference(s):

- [MindGardener ClawHub Skill Page](https://clawhub.ai/widingmarcus-cyber/skills/mindgardener)
- [MindGardener GitHub Project](https://github.com/widingmarcus-cyber/mindgardener)
- [MindGardener PyPI Package](https://pypi.org/project/mindgardener/)
- [Architecture](docs/ARCHITECTURE.md)
- [Research Background](docs/RESEARCH.md)
- [State Tracker Integration](docs/state-tracker-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated memory artifacts are Markdown and JSONL files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the garden CLI. LLM-backed extraction, surprise scoring, and consolidation depend on the configured provider; recall and context assembly operate on local files.]

## Skill Version(s):

1.1.0 (source: release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
