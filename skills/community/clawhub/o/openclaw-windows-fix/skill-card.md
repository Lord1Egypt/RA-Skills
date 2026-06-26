## Description: <br>
Fixes the Windows scheduled task bug that kills OpenClaw processes during idle. One script, permanent fix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to repair a Windows Scheduled Task configuration that can stop the OpenClaw Gateway after idle periods. It provides either a batch command sequence or manual Task Scheduler steps to recreate the task with logon startup, highest privileges, restart-on-failure behavior, and no idle stop condition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The batch script deletes and recreates the existing OpenClaw Gateway scheduled task with highest privileges and persistent logon startup behavior. <br>
Mitigation: Review the commands before running them, export or record any customized task settings first, and run the script only when replacing that scheduled task is intended. <br>


## Reference(s): <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/openclaw-windows-fix) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with an inline Windows batch script and manual Task Scheduler steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review and administrator execution on Windows before changing the existing OpenClaw Gateway scheduled task.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
