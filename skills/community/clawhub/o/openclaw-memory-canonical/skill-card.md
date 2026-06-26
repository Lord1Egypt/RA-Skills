## Description: <br>
Lightweight file-based memory system for single-user AI agents that uses markdown memory tiers, helper scripts, health checks, compaction recovery, archival, and review routines to maintain durable workspace memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give a single-user AI agent durable local workspace memory, including active working state, episodic notes, semantic/procedural files, learnings, health checks, and archival routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to create and update durable local workspace memory files. <br>
Mitigation: Install and invoke it only for workspaces where persistent agent memory is wanted; avoid using it for purely theoretical memory discussions if file changes are not desired. <br>
Risk: Bundled helper scripts may overwrite or diverge from already deployed runtime scripts when copied into memory/scripts. <br>
Mitigation: Review and diff the bundled scripts before syncing, back up local custom scripts, then run the health check after syncing. <br>
Risk: Local memory files can accidentally retain sensitive information if an agent records it. <br>
Mitigation: Review memory contents before sharing a workspace and follow the skill guidance to avoid storing credentials in episodic notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ciklopentan/openclaw-memory-canonical) <br>
- [Publisher profile](https://clawhub.ai/user/ciklopentan) <br>
- [Design rationale](references/design-rationale.md) <br>
- [Verification evidence](references/verification-evidence.md) <br>
- [Reference test log](references/reference-test-log.md) <br>
- [Upgrade guide](UPGRADE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file layout conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace memory files and helper-script usage guidance; no external service output is required.] <br>

## Skill Version(s): <br>
4.6.14 (source: server release evidence and CHANGELOG top entry, released 2026-04-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
