## Description: <br>
Build and run multi-agent content production teams on OpenClaw using a single-repo architecture, symlink-based file sharing, role-specific AGENTS.md files, and review-fix-score loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonlin1212](https://clawhub.ai/user/simonlin1212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to set up OpenClaw agent teams with writer, reviewer, scorer, and fixer roles. It helps bootstrap workspaces, configure spawn permissions, and run repeated review-fix-score cycles until content reaches a quality threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script creates or updates OpenClaw workspaces under ~/.openclaw and prints configuration changes for openclaw.json. <br>
Mitigation: Review scripts/setup-team.sh before running it and back up ~/.openclaw/openclaw.json before applying any generated configuration. <br>
Risk: Granting broad subagent permissions can let the main agent spawn roles beyond the intended team. <br>
Mitigation: Grant allowAgents only to the specific writer, reviewer, scorer, and fixer agent IDs required for the workflow. <br>
Risk: Shared OUTPUT, KNOWLEDGE, and AGENTS.md files may be visible to multiple spawned roles through the workspace layout. <br>
Mitigation: Do not place secrets or private material in shared files unless every spawned role is intended to see it. <br>
Risk: Ambiguous or untrusted agent IDs can make workspace creation and permission review harder to audit. <br>
Mitigation: Use simple trusted agent IDs and inspect generated workspace paths before starting production runs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/simonlin1212/openclaw-agent-team-orchestration) <br>
- [Architecture](references/architecture.md) <br>
- [Build Guide](references/build-guide.md) <br>
- [Workflow](references/workflow.md) <br>
- [Role Templates](references/role-templates.md) <br>
- [Lessons Learned](references/lessons-learned.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw workspace setup guidance, role templates, workflow patterns, and a local setup script.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
