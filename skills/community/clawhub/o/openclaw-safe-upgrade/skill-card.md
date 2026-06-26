## Description: <br>
Safe OpenClaw upgrade with instant rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliahmadaziz](https://clawhub.ai/user/aliahmadaziz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and operators use this skill to check for updates, run a guarded OpenClaw upgrade, preserve configuration and cron state, restart the gateway, and roll back when critical checks fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upgrade script can modify the OpenClaw installation, restart the gateway, and read or restore OpenClaw and acpx configuration. <br>
Mitigation: Run the read-only --check mode first, review the reported upgrade path with the user, and keep the rollback backup available until the upgrade result is confirmed. <br>
Risk: The script can automatically run workspace helper scripts when service-quick-check.py or golden-snapshot.sh exists. <br>
Mitigation: Inspect or remove workspace helper scripts before a full upgrade when their behavior is not already trusted. <br>
Risk: The script can automatically add, commit, and push workspace git changes after a successful upgrade. <br>
Mitigation: Disable or review the git add, commit, and push block before running a full upgrade in repositories where automatic publishing is not desired. <br>


## Reference(s): <br>
- [OpenClaw Safe Upgrade release](https://clawhub.ai/aliahmadaziz/openclaw-safe-upgrade) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash commands and result-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance and directs the agent to inspect local log and result files after the gateway restart.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
