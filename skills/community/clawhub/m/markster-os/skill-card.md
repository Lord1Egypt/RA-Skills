## Description: <br>
Lightweight guide and router for Markster OS that explains the system, points users to the full Git-backed workspace setup, and helps decide whether to approve installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atiti](https://clawhub.ai/user/atiti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small-team operators use this bootstrap skill to understand Markster OS, review the setup path, initialize a Git-backed company workspace, and hand off to the local runtime skill after installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The full setup fetches and runs an installer from an external repository branch that may change over time. <br>
Mitigation: Review the external repository and install.sh before approving the full installation. <br>
Risk: Git remote or push actions could publish secrets, private notes, customer data, or other unintended company information from the workspace. <br>
Mitigation: Inspect the workspace before any commit or push and require explicit user approval before remote or push commands. <br>


## Reference(s): <br>
- [Markster OS repository](https://github.com/markster-public/markster-os) <br>
- [OpenClaw guide](https://github.com/markster-public/markster-os/blob/master/setup-prompts/openclaw.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit approval before install, remote, or push commands and hands off to the local runtime skill after setup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
