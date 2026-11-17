## Description:

Harden Hostinger VPS deployments running OpenClaw agents with firewall lockdown, SSH hardening, Fail2Ban, loopback binding, Cloudflare Tunnel and Access, unattended security upgrades, and file permission hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to secure publicly deployed OpenClaw instances on Hostinger VPS servers. It guides Cloudflare-based access control, server hardening, and operational checks that reduce direct exposure and brute-force risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The root-level hardening script can change SSH, firewall, package, service, and file permission settings on a VPS.

Mitigation: Audit the script first, run the documented dry run, and keep provider console access or backups available before applying changes.

Risk: Firewall and SSH changes can lock out administrators if Cloudflare Tunnel, SSH keys, or the new SSH port are not verified first.

Mitigation: Confirm the Cloudflare Tunnel is active, verify a non-root sudo account and SSH key, and test SSH on the new port in a separate terminal before closing the existing session.

Risk: Untrusted script arguments could be unsafe in a root-level shell workflow.

Mitigation: Use trusted values for script options and avoid passing unreviewed or user-supplied arguments.

Risk: Cloudflare Access service-token secrets embedded in a shipped mobile app could be extracted and reused.

Mitigation: Do not embed service-token secrets in distributed clients; rotate and revoke tokens when exposure is suspected.

## Reference(s):

- [OpenClaw VPS Server Hardening on ClawHub](https://clawhub.ai/maverick-software/skills/openclaw-vps-hardening)
- [Cloudflare Access Setup - Per-Agent Identity Gate](references/cloudflare-access.md)
- [Threat Model & Attack Surface](references/threat-model.md)
- [Cloudflare Zero Trust Services Plans](https://www.cloudflare.com/plans/zero-trust-services/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an optional root-level shell script workflow with dry-run and skip flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
