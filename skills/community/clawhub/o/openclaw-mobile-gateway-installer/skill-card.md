## Description: <br>
Installs and manages OpenClaw mobile gateway as a system service. Invoke when users need one-command deploy, start, stop, upgrade, or uninstall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason141123-sys](https://clawhub.ai/user/jason141123-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, upgrade, check, restart, and uninstall an OpenClaw mobile administration gateway as a systemd service. It is intended for hosts where a network-accessible gateway on port 4800 is acceptable and can be protected appropriately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed service exposes a broad administrative API and sensitive controls on a network-accessible gateway. <br>
Mitigation: Install only on intended hosts, restrict port 4800 with a firewall or authenticated reverse proxy, and review who can call the API. <br>
Risk: Gateway tokens or upstream authorization values may be stored in /etc/openclaw-mobile-gateway/env. <br>
Mitigation: Protect the environment file, limit host access, and rotate any stored token after testing or if exposure is suspected. <br>
Risk: The gateway can read or write OpenClaw configuration paths selected through environment variables. <br>
Mitigation: Inspect OPENCLAW_CONFIG_PATH, OPENCLAW_RUNTIME_CONFIG_PATH, and OPENCLAW_USAGE_CONFIG_PATH before installation and run with the least suitable service account. <br>
Risk: The uninstall script removes the configured install directory recursively. <br>
Mitigation: Do not run uninstall.sh with a custom INSTALL_DIR unless the target path has been verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jason141123-sys/openclaw-mobile-gateway-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing install, check, service-management, and uninstall guidance for a packaged gateway.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
