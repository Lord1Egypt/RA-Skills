## Description: <br>
Installs and configures OpenClaw on remote servers over SSH, with automatic selection among installer, Docker, Podman, npm, and pnpm methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system administrators use this skill to deploy OpenClaw to VPS, cloud, or multi-machine environments and to configure model credentials, channels, and gateway settings after installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands and change configuration on remote hosts. <br>
Mitigation: Use it only against servers you control and review the planned remote installation or configuration action before execution. <br>
Risk: SSH credentials and model provider API keys can be exposed through command-line arguments, host verification choices, logs, or plaintext configuration. <br>
Mitigation: Prefer SSH keys, verify host fingerprints, use environment-variable references for secrets, avoid command-line passwords or API keys, and protect or delete generated logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/openclaw-remote-install) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local installation logs under ~/.openclaw/remote-install-logs/ when the bundled scripts run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
