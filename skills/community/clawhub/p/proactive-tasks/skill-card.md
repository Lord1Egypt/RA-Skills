## Description: <br>
Proactive Tasks helps agents manage goals, break projects into tasks, track progress, and work autonomously on objectives during heartbeat checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImrKhn03](https://clawhub.ai/user/ImrKhn03) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, team leads, and autonomous-agent users use this skill to plan goals, track task progress, manage blockers, and let agents make bounded progress during scheduled heartbeat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous task checks can continue work without a fresh user prompt. <br>
Mitigation: Enable heartbeat or cron only for named approved projects, keep actions bounded, and require approval for external, irreversible, or sensitive operations. <br>
Risk: Task notes and state files may capture sensitive project details in the workspace. <br>
Mitigation: Avoid storing secrets or sensitive business details in task notes, and periodically review or clear SESSION-STATE.md, working-buffer.md, and memory files. <br>
Risk: Shared task and memory files can become stale or inconsistent during autonomous operation. <br>
Mitigation: Run the documented health-check workflow and review task state before relying on autonomous progress reports. <br>


## Reference(s): <br>
- [Proactive Tasks README](README.md) <br>
- [Heartbeat Configuration](HEARTBEAT-CONFIG.md) <br>
- [Release Changelog](CHANGELOG.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ImrKhn03/proactive-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON or markdown state files when task commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can write task data, session state, working-buffer, and memory files in the local workspace.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata; artifact package.json and CHANGELOG report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
