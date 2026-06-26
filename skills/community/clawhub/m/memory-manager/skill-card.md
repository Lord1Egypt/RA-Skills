## Description: <br>
Local memory management for agents with compression detection, snapshots, semantic search, historical memory search, and memory usage tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marmikcfc](https://clawhub.ai/user/marmikcfc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Memory Manager to create a local three-tier memory workspace, detect compression risk, snapshot important context, organize memory files, and retrieve prior work by memory type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory organization and categorization can move, copy, or append local memory content. <br>
Mitigation: Review target memory files before running organize.sh, snapshot.sh, or categorize.sh, and keep backups for content that should not be changed automatically. <br>
Risk: Snapshots and memory files may preserve sensitive local context if secrets are stored in the workspace memory directory. <br>
Mitigation: Avoid storing secrets in memory files, and periodically review snapshots and legacy folders for sensitive or obsolete content. <br>


## Reference(s): <br>
- [Memory Manager ClawHub Page](https://clawhub.ai/marmikcfc/memory-manager) <br>
- [README](artifact/README.md) <br>
- [Moltbook Agent Skills Community](https://www.moltbook.com/m/agentskills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Shell command output and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, moves, copies, appends, searches, and summarizes local memory files under the configured OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
