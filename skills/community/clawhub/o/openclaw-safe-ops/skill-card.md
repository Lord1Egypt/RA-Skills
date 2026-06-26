## Description: <br>
Guards high-risk OpenClaw operations with preflight backups, post-change health checks, and rollback guidance for gateway, configuration, plugin, and openclaw.json changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhrxy](https://clawhub.ai/user/dhrxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill before risky OpenClaw gateway, configuration, plugin, or openclaw.json changes to capture backups, run health checks, and report rollback status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends a local wrapper script that is not included in the release artifact. <br>
Mitigation: Inspect the exact local ./scripts/openclaw-safe.sh before use, or run the documented backup, command, and health-check steps manually. <br>
Risk: The rollback example may restore a different backup file than the one created before the change. <br>
Mitigation: Record the backup path created for the operation and restore that exact file during rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dhrxy/openclaw-safe-ops) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dhrxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports command executed, backup path used, health check results, and whether rollback was needed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
