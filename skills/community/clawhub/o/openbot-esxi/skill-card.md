## Description:

Zero-touch Debian 13 VM deployment on VMware ESXi 8 that builds a custom preseed ISO, creates an NVMe and vmxnet3 VM with serial console access, and runs unattended installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cepheiden](https://clawhub.ai/user/cepheiden)

### License/Terms of Use:


## Use Case:

Developers and infrastructure engineers use this skill to deploy Debian VMs on ESXi, automate VM provisioning, configure serial console access, and resize VM disks online.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-level ESXi and VM access can expose credentials or damage infrastructure if run in an unreviewed environment.

Mitigation: Review before installation, test in a lab or tightly controlled admin network, validate all inputs, and avoid ESXi root where possible.

Risk: Credentials and generated VM passwords may be exposed through stdout, uploaded preseed ISOs, password-based SSH, or persistent environment variables.

Mitigation: Treat output as sensitive, use SSH keys or a credential store for production use, delete uploaded preseed ISOs after deployment, and avoid persistent root passwords.

Risk: Disabled TLS and SSH host-key verification plus an unencrypted telnet serial console can allow interception or unauthorized console access on reachable admin networks.

Mitigation: Enable certificate and SSH host-key verification, restrict or disable the ESXi remote serial port firewall rule, and segment serial-console access behind trusted networks or VPN.

Risk: The Debian installer ISO is downloaded automatically and may not be validated before use.

Mitigation: Verify Debian ISO checksums before building deployment media.

## Reference(s):

- [Preseed Template](references/preseed-template.cfg)
- [VMX Configuration Reference](references/vmx-template.md)
- [govmomi/govc](https://github.com/vmware/govmomi)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/cepheiden/skills/openbot-esxi)
- [ClawHub Publisher Profile](https://clawhub.ai/user/cepheiden)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment steps, environment-variable guidance, command invocations, and configuration references for ESXi Debian VM automation.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
