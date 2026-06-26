## Description: <br>
Create Ubuntu 24.04 VMs on Windows Hyper-V from cloud images with cloud-init, including sparse VHDX handling, Hyper-V network configuration, permissions, Secure Boot settings, and Docker Compose v2 setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to create Docker-ready Ubuntu virtual machines on Windows Hyper-V hosts. It is intended for fresh VM provisioning where SSH access, cloud-init configuration, and Hyper-V administrator actions are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Administrator-level Hyper-V actions can change or remove infrastructure on the target host. <br>
Mitigation: Manually confirm the host, VM name, VHDX path, and command intent before execution, especially before any destroy operation. <br>
Risk: VM password handling can expose credentials in chat logs, shell history, or process lists. <br>
Mitigation: Prefer SSH keys or a throwaway credential, pass passwords through VM_PASSWORD or stdin, and avoid returning passwords in final chat output. <br>
Risk: The release evidence notes missing bundled PowerShell scripts referenced by the skill text. <br>
Mitigation: Do not substitute unreviewed replacement PowerShell scripts; review any host-side script before running it with elevated privileges. <br>


## Reference(s): <br>
- [Hyper-V VM creation defaults](references/defaults.md) <br>
- [Hyper-V VM creation gotchas](references/gotchas.md) <br>
- [Ubuntu 24.04 cloud image](https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img) <br>
- [Docker Compose v2.32.4 binary](https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64) <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/hyperv-create-vm) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/solomonneas) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces VM creation steps and return values such as VM name, IP address, SSH target, and Docker readiness.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
