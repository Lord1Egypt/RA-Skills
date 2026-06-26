## Description: <br>
Multica Manager helps an agent assign, monitor, control, and summarize work across named Multica agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy-gaoyue](https://clawhub.ai/user/andy-gaoyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers use this skill to delegate work to Multica agents, check progress, control running tasks, and summarize completed results for the requester. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or control Multica tasks and forward content to agent sessions with broad authority. <br>
Mitigation: Require explicit confirmation before task creation, stop or restart commands, and session-message fallback. <br>
Risk: Task titles, messages, and local task logs may contain sensitive information. <br>
Mitigation: Avoid secrets or sensitive business details in delegated task content and periodically review or clear local Multica task logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy-gaoyue/multica-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Multica issues, query agent status, write local task logs, and use a session-message fallback when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
