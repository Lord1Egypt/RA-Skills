## Description: <br>
Installs and configures the OpenViking long-term memory plugin for OpenClaw, including prerequisite checks, plugin installation, wizard configuration, gateway restart, verification, and uninstall guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linqiang391](https://clawhub.ai/user/linqiang391) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, verify, operate, and uninstall OpenViking long-term memory for an existing OpenViking server through guided conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed plugin can archive OpenClaw conversation content to an OpenViking server for later recall. <br>
Mitigation: Use only with a trusted OpenViking server and avoid testing with real sensitive data unless that storage and recall behavior is intended. <br>
Risk: The setup may require an API key for the OpenViking server. <br>
Mitigation: Prefer a scoped user API key instead of a broad root key, and provide account and user IDs when root-key multi-tenant scoping is required. <br>
Risk: The fallback installer path downloads and installs a package through npm if ClawHub installation is unavailable. <br>
Mitigation: Review the fallback path before use when policy requires installation only through ClawHub. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linqiang391/install-openviking-memory) <br>
- [OpenViking project homepage](https://github.com/volcengine/OpenViking) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects a server URL, optional API key, optional agent prefix, and conditional account and user IDs for root-key deployments.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
