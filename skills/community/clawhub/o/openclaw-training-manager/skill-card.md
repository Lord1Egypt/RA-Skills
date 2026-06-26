## Description: <br>
Manage and optimize your OpenClaw training workspace -- scaffold files, generate skills, log training sessions, and validate workspace structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anova44](https://clawhub.ai/user/anova44) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up, train, inspect, back up, and maintain an OpenClaw workspace through guided commands and workspace health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes workspace files that can shape future agent behavior. <br>
Mitigation: Preview and review changes to AGENTS.md, SOUL.md, USER.md, TOOLS.md, IDENTITY.md, MEMORY.md, and generated skills before relying on them. <br>
Risk: Training notes and memory files may contain sensitive personal or project information. <br>
Mitigation: Avoid storing secrets or sensitive personal information, and review memory files and exported backups before sharing or syncing them. <br>
Risk: Large training or consolidation changes can replace or reorganize important workspace context. <br>
Mitigation: Create or keep backups before large setup, training, consolidation, or export operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anova44/openclaw-training-manager) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command output, with generated workspace files and backup archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash on Linux or macOS and uses OPENCLAW_WORKSPACE when set.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
