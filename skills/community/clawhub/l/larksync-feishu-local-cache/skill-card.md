## Description: <br>
Syncs Feishu documents into a local cache so OpenClaw agents can read local copies first and reduce repeated Feishu API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooderno1](https://clawhub.ai/user/gooderno1) <br>

### License/Terms of Use: <br>
CC-BY-NC-SA-4.0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure low-frequency Feishu folder synchronization into local Markdown and file caches. It is intended for local-first document retrieval, status checks, and controlled sync task setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The WSL helper can send Feishu folder tokens to an auto-selected non-local backend. <br>
Mitigation: Verify the printed base URL before creating tasks or bootstrapping daily sync, and use only explicit trusted localhost or host addresses. <br>
Risk: Enabled sync tasks can affect Feishu content if upload-capable modes are selected. <br>
Mitigation: Keep download_only unless upload_only or bidirectional sync is deliberately requested, and review or delete scheduled sync tasks when they are no longer needed. <br>
Risk: The skill depends on a trusted LarkSync service and completed Feishu authorization. <br>
Mitigation: Install only if the LarkSync service is trusted, confirm OAuth status with check before task changes, and require user action for first-time Feishu authorization. <br>


## Reference(s): <br>
- [LarkSync homepage](https://github.com/gooderno1/LarkSync) <br>
- [ClawHub skill page](https://clawhub.ai/gooderno1/larksync-feishu-local-cache) <br>
- [OpenClaw agent guide](OPENCLAW_AGENT_GUIDE.md) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and helper JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts return JSON for agent orchestration and audit trails.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
