## Description: <br>
Memory Manager helps agents initialize, organize, search, snapshot, and monitor local episodic, semantic, and procedural memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep local agent memory structured, searchable, and recoverable during long-running work. It is intended for managing memory files, detecting context-compression risk, creating local snapshots, and migrating flat memory notes into episodic, semantic, and procedural folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, write, snapshot, and reorganize local agent memory, which may include private working context. <br>
Mitigation: Back up the memory directory before running organize or categorize, review the affected files after migration, and keep sensitive data out of memory files. <br>
Risk: Snapshots copy selected memory content into plaintext Markdown files. <br>
Mitigation: Store snapshots only in trusted local workspaces, review their contents, and delete stale snapshots according to the user's retention needs. <br>
Risk: Heartbeat-style automation can trigger memory checks or snapshots repeatedly before the operator has reviewed behavior. <br>
Mitigation: Run the scripts manually first, inspect the generated state and snapshot files, and enable automation only after the workflow is understood. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onlyloveher/memory-manager-clawd) <br>
- [Moltbook agentskills community](https://www.moltbook.com/m/agentskills) <br>
- [Legacy ClawHub skill homepage](https://clawhub.com/skills/memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell command output and local Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reorganizes local memory files under the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
