## Description: <br>
MemCore is a five-tier adaptive memory system for OpenClaw agents that indexes local memories, retrieves relevant context on demand, generates compact startup briefs, and supports feedback-driven pattern induction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adchina2025](https://clawhub.ai/user/adchina2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use MemCore to replace full MEMORY.md startup loading with a compact MEMORY_BRIEF.md, search historical memory on demand, run maintenance indexing, induce recurring patterns, and support report-only health diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MemCore can immediately process and persist sensitive OpenClaw workspace memories, session state, search queries, and generated summaries. <br>
Mitigation: Install only in a trusted local OpenClaw workspace, back up ~/.openclaw before use, and review the local SQLite indexes and generated summaries as durable memory records. <br>
Risk: Scheduled maintenance or meeting-end automation can index fresh workspace memory without active review. <br>
Mitigation: Enable cron and automated maintenance only after deciding that the retention behavior is acceptable; keep health checks report-only and review generated briefs before relying on them. <br>


## Reference(s): <br>
- [MemCore architecture](references/architecture.md) <br>
- [MemCore upgrade guide](references/upgrade-guide.md) <br>
- [MemCore usage guide](references/使用说明.md) <br>
- [ClawHub release page](https://clawhub.ai/adchina2025/memcore-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates MEMORY_BRIEF.md capped at about 500 tokens and maintains local SQLite indexes under ~/.openclaw.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md description) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
