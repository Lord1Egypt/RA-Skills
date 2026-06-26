## Description: <br>
Deploy OpenClaw with a cloud gateway using Tailscale and SSH tunneling, including environment checks, firewall setup, service installation, and diagnostic commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarsHong-86](https://clawhub.ai/user/MarsHong-86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose and run guided OpenClaw deployment plans for Linux cloud gateways and Windows local clients. It is intended for cloud gateway, remote node, and two-way sync setups that require Tailscale, firewall configuration, systemd services, and troubleshooting output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment scripts install persistent network services that run as root and expose gateway ports. <br>
Mitigation: Use a dedicated host, review the scripts before execution, consider a non-root service account, and restrict firewall and cloud security-group access to Tailscale or known source IPs. <br>
Risk: Remote gateway mode can use insecure private WebSocket settings and --allow-unconfigured. <br>
Mitigation: Remove or justify those settings before production use and verify authentication, bind addresses, and network exposure. <br>
Risk: Generated tokens and diagnostic output may expose access details or host information. <br>
Mitigation: Protect and rotate generated tokens, and review diagnostic output before sharing it. <br>
Risk: The documented installation flow includes curl-to-shell style dependency installation. <br>
Mitigation: Prefer package-manager or pinned-source installation where possible, and inspect downloaded scripts before running them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MarsHong-86/openclaw-two-way-deployment) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Diagnostics] <br>
**Output Format:** [Markdown with bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment plans, generated service and OpenClaw configuration, tokens, firewall guidance, and diagnostic output for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
