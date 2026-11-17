## Description:

Agent workspace memory lifecycle management via 10 MCP tools and batch maintenance for MEMORY.md, memory directories, meta.json, quality gates, Bayesian decay, case lifecycle, and compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5rbdmak7f-alt](https://clawhub.ai/user/5rbdmak7f-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, configure, inspect, and maintain local workspace memory stores through MCP tools, CLI commands, and scheduled batch workflows. It supports memory ingestion, decay, compaction, synchronization, quality checks, and case review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-boundary validation weakness may allow crafted memory metadata to create files outside the intended workspace.

Mitigation: Use only trusted workspaces, review memory/meta.json before running maintenance, and patch path validation so memory files resolve under the intended workspace/memory directory before enabling cron maintenance.

Risk: Batch maintenance and decay operations can modify or retire workspace memory records.

Mitigation: Run dry-run checks first, keep workspace backups, and require human review for destructive or high-impact case lifecycle changes.

## Reference(s):

- [Memory Guardian ClawHub Listing](https://clawhub.ai/5rbdmak7f-alt/skills/memory-guardian-agent)
- [Signal Loop](references/signal-loop.md)
- [Triggers](references/triggers.md)
- [Parameters](references/parameters.md)
- [Compaction](references/compaction.md)
- [Error Recovery](references/error_recovery.md)
- [Case Management](references/case-management.md)
- [Advanced Tools](references/advanced-tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and tool-call recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dry-run or apply operations that read or modify local workspace memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
