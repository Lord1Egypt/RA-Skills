## Description: <br>
Manage long-running Cursor CLI coding tasks through OpenClaw tools backed by tmux sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangzeyu99-web](https://clawhub.ai/user/zhangzeyu99-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to start, monitor, send instructions to, and stop persistent Cursor CLI coding tasks from OpenClaw when work needs to continue in tmux rather than a short inline session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives OpenClaw broad control over trusted background Cursor coding sessions. <br>
Mitigation: Install only when you intentionally want OpenClaw to start and control trusted Cursor sessions, and review diffs before accepting changes. <br>
Risk: Exposing the control path publicly could allow unwanted access to local coding sessions. <br>
Mitigation: Keep it bound to localhost or a private authenticated network, and use strong authentication and firewall rules before any broader exposure. <br>
Risk: Task inputs, project paths, and logs can contain sensitive project information. <br>
Mitigation: Use trusted project paths and task inputs, treat task logs as sensitive, and back up important work before long-running sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangzeyu99-web/openclaw-cursor-agent) <br>
- [OpenClaw Cursor Agent README](README.md) <br>
- [OpenClaw Cursor Agent usage guide](docs/usage-guide.md) <br>
- [Plugin README](extensions/openclaw-cursor-agent/README.md) <br>
- [Command patterns](extensions/openclaw-cursor-agent/skill/references/commands.md) <br>
- [Cursor agent system README](cursor-agent-system/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text and JSON tool results, with Markdown command examples in references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session names, task IDs, progress, recent output, tmux status, and dependency diagnostics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
