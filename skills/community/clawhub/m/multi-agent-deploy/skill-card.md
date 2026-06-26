## Description: <br>
Deploys a new OpenClaw assistant agent by selecting the next assistant number, copying the template workspace, creating the agent directory, and updating the OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhou19931993](https://clawhub.ai/user/zhou19931993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who manage OpenClaw deployments use this skill when they explicitly want to add another persistent assistant agent while reusing the existing workspace and agent directory layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes persistent OpenClaw configuration changes and creates local workspace and agent directories. <br>
Mitigation: Back up ~/.openclaw/openclaw.json, inspect the generated paths, and review the configuration before restarting the gateway. <br>
Risk: Security evidence reports a path bug that can create files outside the documented location. <br>
Mitigation: Fix or account for the workspace path mismatch before deployment and verify the resulting workspace and agentDir values. <br>
Risk: Broad natural-language triggers may create a new persistent assistant when that is not intended. <br>
Mitigation: Use the skill only after the user explicitly asks to create or deploy a new assistant agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhou19931993/multi-agent-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local OpenClaw workspace, agent directory, and configuration changes when the deployment script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
