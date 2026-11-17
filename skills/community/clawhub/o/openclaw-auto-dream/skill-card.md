## Description:

Cognitive memory architecture for OpenClaw agents that runs periodic dream cycles to consolidate daily logs into structured long-term memory with importance scoring, insights, and push notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myclaw-ai](https://clawhub.ai/user/myclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to initialize and run recurring memory consolidation over their workspace memory logs. It helps maintain long-term memory files, dream reports, stale-thread reminders, health scoring, dashboards, and migration bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently reads and rewrites broad memory history in the workspace.

Mitigation: Review the cron schedule before enabling it, keep backups of memory files, and install only where recurring memory consolidation is intended.

Risk: Imported memory bundles can introduce untrusted or unwanted content into long-term memory.

Mitigation: Do not import memory bundles from untrusted sources, and test selective imports before performing a full import.

Risk: Generated dashboards may expose or render memory-derived content.

Mitigation: Avoid opening, sharing, or publishing generated dashboards unless memory-derived HTML is sanitized and the content is appropriate to disclose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myclaw-ai/skills/openclaw-auto-dream)
- [MyClaw.ai](https://myclaw.ai)
- [First Dream - Post-Install Memory Scan](artifact/references/first-dream-prompt.md)
- [Auto-Dream Lite - Quick Memory Consolidation](artifact/references/dream-prompt-lite.md)
- [Auto-Dream Cycle - Execution Prompt](artifact/references/dream-prompt.md)
- [Memory Templates](artifact/references/memory-template.md)
- [Scoring and Forgetting](artifact/references/scoring.md)
- [Cross-Instance Memory Migration](artifact/references/migration-cross-instance.md)
- [Migration Guide v1 to v2](artifact/references/migration-v1-to-v2.md)
- [Migration Guide v1 to v2 to v3](artifact/references/migration-v2-to-v3.md)
- [Dashboard Template](artifact/references/dashboard-template.html)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, JSON configuration examples, memory file templates, migration guidance, and generated HTML dashboard content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory artifacts such as MEMORY.md updates, memory index JSON, dream reports, migration bundles, and optional dashboard HTML.]

## Skill Version(s):

4.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
