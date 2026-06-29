## Description: <br>
Detect friction signals and graduate recurring patterns into rules for session retrospectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review session friction, identify recurring correction or retry patterns, and promote reviewed lessons into durable guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local friction logs and learning candidates may capture sensitive session context, including corrections, failed commands, and related details. <br>
Mitigation: Use the skill only in sessions where this local storage is acceptable, and inspect or delete files under ~/.claude/friction and LEARNINGS.md when handling sensitive work. <br>
Risk: Promoted patterns could become incorrect or overly broad guidance if accepted without review. <br>
Mitigation: Review friction reports and require explicit approval before adding permanent guidance to project or user configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-friction-detector) <br>
- [Claude Night Market abstract plugin](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local friction session logs and learning candidates under user-controlled Claude configuration paths.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
