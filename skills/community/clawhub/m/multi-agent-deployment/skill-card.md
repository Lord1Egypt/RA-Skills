## Description: <br>
Deploys a production-ready multi-agent OpenClaw fleet with workspace scaffolding, routing configuration, memory sync, and VPS deployment scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinas90](https://clawhub.ai/user/abhinas90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to stand up role-specific OpenClaw agent workspaces, generate routing configuration, synchronize shared memory sections, and deploy the resulting fleet to a VPS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts can overwrite OpenClaw configuration and agent memory files. <br>
Mitigation: Review the generated files, run first against a staging OpenClaw instance, and back up /data/.openclaw and the VPS data directory before applying changes. <br>
Risk: The deployment script can restart the remote OpenClaw container. <br>
Mitigation: Schedule execution during a maintenance window, verify the target container and VPS data path, and confirm rollback steps before running deploy.sh. <br>
Risk: The deployment workflow uses SSH access to a VPS and may be run as root. <br>
Mitigation: Use a least-privilege SSH account where possible, protect private keys, and avoid root SSH unless the environment explicitly requires it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abhinas90/multi-agent-deployment) <br>
- [Publisher profile](https://clawhub.ai/user/abhinas90) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, and JSON snippets plus helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace scaffolding, OpenClaw routing configuration, memory synchronization behavior, and VPS deployment commands for adaptation before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
