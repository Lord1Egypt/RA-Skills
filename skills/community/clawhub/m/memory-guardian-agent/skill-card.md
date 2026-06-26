## Description: <br>
Agent workspace memory lifecycle management via MCP tools and batch maintenance for MEMORY.md, memory directories, meta.json, quality gates, Bayesian decay, case lifecycle, and compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5rbdmak7f-alt](https://clawhub.ai/user/5rbdmak7f-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, configure, and run scheduled or on-demand workspace memory maintenance. It helps inspect memory status, ingest and query memories, run decay and compaction, review cases, and diagnose memory bloat or quality anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically rewrite, archive, or delete workspace memory. <br>
Mitigation: Install it only in workspaces where automatic memory maintenance is acceptable, keep backups, and run dry-run modes before apply modes. <br>
Risk: Weak confirmation and scoping controls may affect important agent memory. <br>
Mitigation: Use explicit workspace paths, review case retirement behavior, and inspect the security bypass option before relying on it for important memory. <br>
Risk: Local access logs and meta.json can contain sensitive workspace memory data. <br>
Mitigation: Treat access_log.jsonl and meta.json as sensitive local files and restrict workspace access accordingly. <br>


## Reference(s): <br>
- [Signal Loop](references/signal-loop.md) <br>
- [Triggers](references/triggers.md) <br>
- [Parameters](references/parameters.md) <br>
- [Compaction](references/compaction.md) <br>
- [Error Recovery](references/error_recovery.md) <br>
- [Case Management](references/case-management.md) <br>
- [Advanced Tools](references/advanced-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, CLI commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run summaries, maintenance recommendations, memory and case status summaries, and workspace file changes when apply modes are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
