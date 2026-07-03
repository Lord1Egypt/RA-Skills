## Description: <br>
Docker Manager provides Docker container visibility and documented management workflows for container lifecycle, cleanup, resource monitoring, log rotation, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers can use this skill to inspect Docker container names and review Docker management workflows for containers, images, logs, cleanup, and health checks. Advertised cleanup and pruning behavior should be reviewed before use because the artifact implementation primarily lists running containers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact advertises Docker cleanup, pruning, and monitoring features beyond the observed container-listing implementation. <br>
Mitigation: Review the artifact code before relying on cleanup, pruning, or monitoring behavior. <br>
Risk: Docker cleanup and pruning commands can remove containers, images, or other runtime state if expanded or run destructively. <br>
Mitigation: Use explicit backups, filters, and confirmation controls before running destructive Docker operations. <br>
Risk: The package metadata includes unrelated financial referral links. <br>
Mitigation: Treat the metadata links as unrelated to Docker management and review publisher trust before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kingaiwork/king-docker-manager) <br>
- [Publisher profile](https://clawhub.ai/user/kingaiwork) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown usage guidance with bash examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Docker CLI environment for command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
