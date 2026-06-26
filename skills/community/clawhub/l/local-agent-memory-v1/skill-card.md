## Description: <br>
Build, maintain, or improve a layered local memory system for OpenClaw-style agents using markdown files instead of database-backed memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lupinweng](https://clawhub.ai/user/lupinweng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to design and maintain local markdown-based memory layers, consolidate durable facts and workflows, and avoid acting on stale remembered information without re-verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may persist sensitive preferences, environment details, or operational context longer than intended. <br>
Mitigation: Review memory content before storing it and keep memory folders only in workspaces acceptable for persistent local state. <br>
Risk: Stale remembered facts can lead to incorrect actions if treated as authoritative. <br>
Mitigation: Re-check current files, paths, versions, scripts, or environment state before acting on remembered information. <br>
Risk: Large pruning, migration, or restructuring could remove useful memory or reorganize it unexpectedly. <br>
Mitigation: Require explicit user approval before broad cleanup, migration, or restructuring passes and write destination topic files before updating the index. <br>


## Reference(s): <br>
- [Local Agent Memory Architecture](references/architecture.md) <br>
- [Setup and Topic Layout](references/setup.md) <br>
- [Maintenance and Governance](references/maintenance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance and file-structure recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
