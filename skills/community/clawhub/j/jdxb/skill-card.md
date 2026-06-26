## Description: <br>
Manage the 节点小宝 (Node Baby Link / JDxB) remote-access service on Linux, including installation, service control, status checks, logs, pairing codes, updates, and uninstall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skipper-chen](https://clawhub.ai/user/skipper-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a Linux systemd service for JDxB remote access, inspect its health, retrieve pairing details, and run install, update, or uninstall workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install workflow can download unverified code and run it as a persistent root-level remote-access service. <br>
Mitigation: Install only on trusted machines, avoid curl-to-sudo-bash, and prefer a verified vendor package or checksum/signature-checked archive. <br>
Risk: Pairing the service may expose remote-access capability tied to an account or active code. <br>
Mitigation: Review the generated systemd service and pairing details before linking the service to an account. <br>
Risk: Uninstall behavior affects a root-managed systemd service and files under the installation directory. <br>
Mitigation: Review service and file removal behavior before running uninstall on shared or production hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skipper-chen/jdxb) <br>
- [Publisher profile](https://clawhub.ai/user/skipper-chen) <br>
- [JDxB official install script](https://iepose.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require root privileges and can manage a persistent systemd service.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
