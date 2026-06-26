## Description: <br>
AgentGuard routes command, file, and network operations through ag_* tools for rule review, auditing, and sensitive-data redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxz333zxz](https://clawhub.ai/user/zxz333zxz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentGuard to mediate shell commands, file access, network requests, and plugin checks through a local security daemon before an agent action proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a privileged, long-running local daemon to mediate broad command, file, and network operations. <br>
Mitigation: Install only when this mediation is intended, verify the native agentguard binary and checksum/provenance, and review how to stop the daemon and remove /usr/local/bin/agentguard. <br>
Risk: Native tool bypass prevention depends on the user configuring tools.deny before relying on AgentGuard controls. <br>
Mitigation: Confirm tools.deny blocks native command, file, edit, patch, process, and network tools before treating AgentGuard as the enforcement path. <br>
Risk: Pointing daemonHost away from localhost could expose mediated operations to an endpoint the user does not fully trust. <br>
Mitigation: Keep daemonHost on 127.0.0.1 unless the remote endpoint is explicitly trusted and controlled. <br>


## Reference(s): <br>
- [AgentGuard homepage](https://www.agentguard.site) <br>
- [OpenClaw plugin documentation](https://docs.openclaw.ai/tools/plugin) <br>
- [OpenClaw agent tools documentation](https://docs.openclaw.ai/plugins/agent-tools) <br>
- [ClawHub release page](https://clawhub.ai/zxz333zxz/jjy-agentguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [OpenClaw tool responses as text, JSON-formatted daemon responses, and shell/file/network operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local agentguard daemon and binary; artifact metadata supports darwin and linux, and setup.sh supports arm64 only.] <br>

## Skill Version(s): <br>
1.8.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
