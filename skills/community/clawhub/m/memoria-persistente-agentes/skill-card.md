## Description: <br>
Provides a three-layer persistent memory system for AI agents, with core, archival, and recall memory for context continuity across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renateparma](https://clawhub.ai/user/renateparma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents durable memory for user preferences, project context, decisions, and recurring maintenance across sessions. It is suited for agents that need continuity, not for simple question answering with no persistence need. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain personal details, session history, or sensitive context beyond the original conversation. <br>
Mitigation: Use the skill only in workspaces where durable memory is intended, avoid storing health data, secrets, or credential references, and maintain a clear process to inspect, edit, and delete saved memory. <br>
Risk: Session synchronization can read OpenClaw session transcripts from workspace, home, or OPENCLAW_STATE_DIR locations and create a shared session index. <br>
Mitigation: Review or disable session-sync before use, set workspace and state directories deliberately, and run dry-run modes first where available. <br>
Risk: Memory maintenance scripts can write or reorganize files in memory/ and memory/archival/. <br>
Mitigation: Run maintenance commands with dry-run first, review proposed changes, and keep backups or version control for memory files that matter. <br>


## Reference(s): <br>
- [Integration Guide](references/integration.md) <br>
- [ClawHub Release Page](https://clawhub.ai/renateparma/memoria-persistente-agentes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, file templates, and Python utility scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and maintains workspace memory files under memory/ and memory/archival/.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
