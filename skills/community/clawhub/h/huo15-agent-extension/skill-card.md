## Description: <br>
Synchronizes main-agent workspace configuration files and selected directories into dynamic-agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers operating dynamic Agent channels use this skill to copy canonical configuration, memory, and skill directories from the main OpenClaw workspace into per-agent workspaces. It is intended for environments where dynamic agents should inherit the main agent's current configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite persistent agent behavior files in dynamic-agent workspaces. <br>
Mitigation: Review the source and target workspaces before use, keep backups of overwritten files, and prefer a version that supports dry-run or confirmation. <br>
Risk: Dynamic-agent synchronization is not tightly constrained to safe target workspaces. <br>
Mitigation: Use only trusted agentId values and prefer a version that validates agentId and confines resolved write paths to ~/.openclaw/workspace-*. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-agent-extension) <br>
- [Publisher profile](https://clawhub.ai/user/jobzhao15) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, text] <br>
**Output Format:** [Configuration files and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Overwrites selected target configuration files and recursively copies configured directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
