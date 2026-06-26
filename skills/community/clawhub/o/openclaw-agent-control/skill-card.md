## Description: <br>
Deploy and start OpenClaw Agent Control with one command (backend + frontend) using skill-based workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiangAgentLabs](https://clawhub.ai/user/JiangAgentLabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy OpenClaw Agent Control locally, start its backend and frontend, and validate the running service endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment workflow runs unpinned remote code from the configured repository. <br>
Mitigation: Install only when the repository is trusted, and review or pin the source revision before execution. <br>
Risk: The workflow starts persistent backend and frontend services. <br>
Mitigation: Bind services to localhost unless external access is required, and plan how to stop the started processes after use. <br>
Risk: The default project path is under /root and the workflow installs runtime dependencies. <br>
Mitigation: Set PROJECT_DIR to a non-root path when possible and review dependency installation behavior before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JiangAgentLabs/openclaw-agent-control) <br>
- [Publisher profile](https://clawhub.ai/user/JiangAgentLabs) <br>
- [Usage guide (English)](references/USAGE.en.md) <br>
- [Usage guide (Chinese)](references/USAGE.zh-CN.md) <br>
- [OpenClaw Agent Control repository](https://github.com/JiangAgentLabs/OpenClaw-Agent-Control.git) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands, environment variable names, log paths, and local service URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The deployment script starts backend and frontend services when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
