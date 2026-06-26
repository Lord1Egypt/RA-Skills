## Description: <br>
Proactive Trigger evaluates user silence, interest decay, topic heat, and readiness signals to decide when an assistant should intervene proactively. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to evaluate whether a proactive assistant should respond based on silence, topic interest, time windows, and incoming local signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local behavioral history and may create or update .soul state and log files. <br>
Mitigation: Inspect retention expectations before deployment and periodically review or clear the local .soul state and log files. <br>
Risk: The skill trusts shared local OpenClaw signal files. <br>
Mitigation: Restrict which local components can write signals and review signal sources before enabling proactive behavior. <br>
Risk: The skill includes a shell-based OpenClaw command wrapper identified by security evidence as unsafe. <br>
Mitigation: Replace or disable the shell wrapper and review command execution paths before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoguoqiang-hub/proactive-trigger) <br>
- [Proactive trigger system reference](references/SKILL.zh.md) <br>
- [Interest graph calculation](references/interest-graph-calculation.md) <br>
- [Silence index formula](references/silence-index-formula.md) <br>
- [Trigger state management](references/trigger-state-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local OpenClaw .soul state, signal, and log files during use.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
