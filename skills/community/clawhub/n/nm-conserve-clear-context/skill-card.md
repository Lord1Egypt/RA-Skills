## Description: <br>
Manages context overflow by handing off to a fresh subagent at 80% usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill during long-running Claude Code workflows to checkpoint current work, preserve session state, and delegate continuation to a fresh subagent when context pressure becomes high. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can preserve session state and continue automatically in dangerous or unattended modes without fresh user confirmation. <br>
Mitigation: Install only for tightly bounded context handoff workflows, avoid dangerous or unattended use unless the task scope is constrained, and review or delete .claude/session-state.md after sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-clear-context) <br>
- [claude-night-market conserve plugin](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>
- [Session state module](artifact/modules/session-state.md) <br>
- [Session state schema](artifact/modules/session-state-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a session-state markdown checkpoint for continuation agents.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
