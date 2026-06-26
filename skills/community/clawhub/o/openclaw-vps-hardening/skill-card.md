## Description: <br>
Harden a Hostinger VPS running OpenClaw agents with firewall lockdown, SSH hardening, Fail2Ban, loopback binding, Cloudflare Tunnel and Access, unattended security upgrades, and file permission hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to secure a publicly deployed OpenClaw VPS after initial deployment and Cloudflare Tunnel setup. It provides a hardening workflow for reducing exposed network surface, requiring identity-gated access, and protecting SSH and local configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH and firewall changes can lock operators out of the VPS or make agents unreachable if applied before access paths are verified. <br>
Mitigation: Run the dry run first, confirm Cloudflare Tunnel access, verify SSH key and non-root sudo recovery access, keep the old SSH session open, and test the new SSH port in a separate terminal before closing the original session. <br>
Risk: Long-lived Cloudflare Access service-token secrets in a distributed native app can be copied or abused if the app or device is compromised. <br>
Mitigation: Prefer user-bound OIDC/PKCE or a backend-held credential flow; if service tokens are used, keep a rotation, revocation, and containment plan. <br>


## Reference(s): <br>
- [Cloudflare Access Setup](references/cloudflare-access.md) <br>
- [Threat Model and Attack Surface](references/threat-model.md) <br>
- [Cloudflare Zero Trust plans](https://www.cloudflare.com/plans/zero-trust-services/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a root-run hardening script with dry-run and skip options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
