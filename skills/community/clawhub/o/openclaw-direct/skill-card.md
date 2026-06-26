## Description: <br>
One-click OpenClaw installer with security hardening for Windows, macOS, and Linux without Docker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningtoba](https://clawhub.ai/user/ningtoba) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and local automation users use this skill to install OpenClaw, create local LLM gateway configuration, install related ClawHub skills, and start the OpenClaw gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer makes broad local system changes, including global package installs, remote installer execution, persistent local configuration, and background services. <br>
Mitigation: Review setup.sh before running it and use it only in an environment where those changes are acceptable. <br>
Risk: The security evidence flags the release as suspicious because the scope of system changes is partly inconsistent with its safety claims. <br>
Mitigation: Prefer a version that pins dependencies, verifies remote installers, and makes extra skills optional. <br>
Risk: The generated local configuration may contain sensitive API keys if the user adds them later. <br>
Mitigation: Avoid storing sensitive API keys in broadly readable config files and check permissions on the OpenClaw config directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ningtoba/openclaw-direct) <br>
- [Node.js](https://nodejs.org) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with shell commands and generated local JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installer guidance and local OpenClaw configuration; setup may run package installation and service start commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
