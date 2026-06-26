## Description: <br>
Deploys and manages an OpenClaw Connect Enterprise worker node that registers with a Hub, syncs tasks, reports system status, and exposes a local management UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-scarlett](https://clawhub.ai/user/ai-scarlett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run a managed OpenClaw worker node that connects to a remote Hub for task execution, monitoring, memory synchronization, and node administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The node can run as a persistent managed worker with high local authority and execute tasks from a remote Hub. <br>
Mitigation: Install only when the Hub operator is trusted, prefer a dedicated non-root account, and disable or gate task execution when remote execution is not required. <br>
Risk: The local management UI and API may be exposed without authentication. <br>
Mitigation: Bind access behind a firewall or authenticated reverse proxy and require HTTPS for Hub and administrative traffic. <br>
Risk: Credentials and session data are stored in local configuration files. <br>
Mitigation: Restrict permissions on .env and ~/.openclaw-node/node.json, avoid printing secrets, and redact configuration output before sharing logs. <br>
Risk: The node can upload local OpenClaw workspace memory and persona data to the Hub. <br>
Mitigation: Review what workspace data may sync and disable or gate memory/persona synchronization unless it is needed for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-scarlett/openclaw-connect-node) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ai-scarlett) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API descriptions, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, operation, management, and troubleshooting guidance for an OpenClaw worker node.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
