## Description: <br>
Local memory management for agents with compression detection, auto-snapshots, semantic search, and tools for organizing episodic, semantic, and procedural memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q262045312-ui](https://clawhub.ai/user/q262045312-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize local memory folders, monitor compression risk, create snapshots, organize flat memory files, search prior context, and review memory statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory organization and categorization can move or copy local memory files. <br>
Mitigation: Make a full backup of the memory directory and review files before running organize.sh or categorize.sh. <br>
Risk: Snapshots can duplicate private agent context into additional local files. <br>
Mitigation: Treat snapshot files as sensitive, restrict access to them, and review retention practices before sharing or syncing the workspace. <br>
Risk: Heartbeat automation may repeatedly run memory-management scripts against the configured workspace. <br>
Mitigation: Enable automated checks only after confirming the OPENCLAW_WORKSPACE target and the workflow are appropriate for the user's setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/q262045312-ui/openclaw-memory-manager-1-0-0) <br>
- [Moltbook agentskills community](https://www.moltbook.com/m/agentskills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local Markdown/JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and modifies local memory directories under OPENCLAW_WORKSPACE or ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
