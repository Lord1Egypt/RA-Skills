## Description: <br>
Zero-touch Debian 13 VM deployment on VMware ESXi 8. Builds custom preseed ISO, creates NVMe+vmxnet3 VM with serial console, and runs unattended installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cepheiden](https://clawhub.ai/user/cepheiden) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to provision Debian VMs on ESXi, automate VM setup, configure serial-console access, and grow VM disks online. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete and recreate VMs and administer an ESXi host with powerful credentials. <br>
Mitigation: Use a lab or tightly scoped ESXi account where possible, use unique VM names, and review the scripts before execution. <br>
Risk: Host verification defaults are weak for ESXi HTTPS and SSH connections. <br>
Mitigation: Verify ESXi TLS and SSH host identity before running the scripts instead of relying on insecure defaults. <br>
Risk: Generated VM passwords are printed to stdout and embedded in the uploaded preseed ISO. <br>
Mitigation: Protect logs and terminal output that contain generated passwords, then remove the preseed ISO after deployment. <br>
Risk: The telnet serial console is unencrypted and can expose VM console access to hosts that can reach the ESXi serial port. <br>
Mitigation: Restrict the ESXi remoteSerialPort firewall ruleset to trusted networks and disable or remove the serial console when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cepheiden/openbot-esxi) <br>
- [preseed-template.cfg](references/preseed-template.cfg) <br>
- [vmx-template.md](references/vmx-template.md) <br>
- [govmomi govc releases](https://github.com/vmware/govmomi/releases) <br>
- [Debian netinst ISO](https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-13.3.0-amd64-netinst.iso) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment and resize procedures that execute local shell scripts against an ESXi host.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
