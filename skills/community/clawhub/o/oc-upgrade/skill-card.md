## Description: <br>
OpenClaw version upgrade workflow for WSL2 and Linux VM deployments, including environment detection, plugin compatibility checks, backups, validation, restart notification, and rollback guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangsuann](https://clawhub.ai/user/tangsuann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and execute OpenClaw upgrades with preflight environment checks, plugin snapshots, backups, post-upgrade validation, service restart, notification setup, and rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may read local tokens and copy secret-containing configuration files. <br>
Mitigation: Prefer unauthenticated release-note lookup or a least-privilege token, avoid exposing token values in chat, and protect .env backups with owner-only permissions. <br>
Risk: The workflow installs global packages, schedules a one-time notification, and restarts the OpenClaw gateway. <br>
Mitigation: Require explicit operator approval before package installation, cron creation, or service restart, and run during an acceptable maintenance window. <br>
Risk: Rollback commands can delete and restore plugin directories and overwrite configuration files. <br>
Mitigation: Confirm target versions, paths, and backup files before rollback, and stop if required backups are missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangsuann/oc-upgrade) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes upgrade, validation, restart, notification, and rollback command sequences that require operator review before execution.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
