## Description: <br>
Generates an operational resume card before Claude context compaction so the next session knows where it left off, what mode it was in, and what to do next. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nadalpiantini](https://clawhub.ai/user/nadalpiantini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install Claude PreCompact and SessionStart hooks that save a local resume card before context compaction and reload it at the next session start. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local transcript backups and resume cards may contain sensitive prompt or project context. <br>
Mitigation: Use the skill only in workspaces where local context retention is acceptable, avoid secrets in prompts, and add thinking/session-logs/ plus .claude/session-resume-card.md to .gitignore when needed. <br>
Risk: SessionStart automatically reloads the saved resume card into future sessions. <br>
Mitigation: Remove or disable the hooks when automatic context reloads are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nadalpiantini/pre-compact-resume-card) <br>
- [settings-example.json](references/settings-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown resume card and shell hook output with JSON hook configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local .claude/session-resume-card.md file and keeps recent transcript backups under thinking/session-logs/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
