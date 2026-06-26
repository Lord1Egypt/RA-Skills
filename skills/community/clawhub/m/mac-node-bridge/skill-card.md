## Description: <br>
Bridge macOS-only tools into a Linux OpenClaw gateway via SSH wrappers and connected Mac nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect Linux OpenClaw gateways to trusted Mac nodes for macOS-only command-line tools such as imsg, remindctl, memo, things, peekaboo, brew-backed CLIs, and other node-local binaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates SSH wrappers that let a Linux gateway run selected tools on a trusted Mac over SSH. <br>
Mitigation: Install only for trusted Mac nodes, use a dedicated non-root Mac account and SSH key, and keep each wrapper scoped to a specific tool. <br>
Risk: Wrapper access or SSH credentials may remain after the bridge is no longer needed. <br>
Mitigation: Remove the relevant wrapper and revoke or rotate the associated SSH key during rollback. <br>


## Reference(s): <br>
- [Mac Node Bridge on ClawHub](https://clawhub.ai/matthewxmurphy/mac-node-bridge) <br>
- [Publisher Profile](https://clawhub.ai/user/matthewxmurphy) <br>
- [Security Model](references/security-model.md) <br>
- [Publish Pattern](references/publish-pattern.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wrapper installation, verification, and publication guidance for a Linux gateway and trusted Mac nodes.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
