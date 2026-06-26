## Description: <br>
Permission Guard monitors OpenClaw agent skill activity for unauthorized file access, suspicious outbound network calls, dangerous command patterns, and permission audit reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyhetech](https://clawhub.ai/user/billyhetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect agent activity, review permission-sensitive behavior, establish first-run baselines after installing skills, and generate actionable security audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local audit records and baselines that may reveal sensitive operational history or metadata about credential locations. <br>
Mitigation: Review or change baseline behavior before use, protect the ~/.openclaw audit files, and periodically delete records that are no longer needed. <br>
Risk: Filesystem and network inspection require shell access and can surface sensitive local paths or active connection details. <br>
Mitigation: Use the skill only where local security inspection is intended, and review generated findings before sharing or acting on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/billyhetech/permission-guard-v1) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown activity report with shell command recommendations and local audit log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local ~/.openclaw audit logs and baselines when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
