## Description: <br>
Moses Coordinator is a lightweight daemon that monitors OpenClaw Gateway WebSocket session events, detects Primary to Secondary to Observer sequence violations, and logs them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunrisesIllNeverSee](https://clawhub.ai/user/SunrisesIllNeverSee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local OpenClaw session monitor that watches agent ordering, reports sequence violations, and records audit events for the Moses governance workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The coordinator may run as a background process and continuously monitor local session events. <br>
Mitigation: Install it only when a persistent local session monitor is intended, and run it under a user account with appropriate local permissions. <br>
Risk: The coordinator executes an audit helper from the user's home directory. <br>
Mitigation: Review the referenced helper script before use, confirm it is owned by the user, and ensure it is not writable by other users. <br>
Risk: The release does not include server-resolved source provenance for this version. <br>
Mitigation: Use the ClawHub release evidence and artifact hashes for review, and do not rely on inferred GitHub provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SunrisesIllNeverSee/moses-coordinator) <br>
- [Publisher profile](https://clawhub.ai/user/SunrisesIllNeverSee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local monitor output and audit-log actions when the coordinator is run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
