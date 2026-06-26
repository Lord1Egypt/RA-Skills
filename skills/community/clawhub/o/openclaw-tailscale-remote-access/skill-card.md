## Description: <br>
Configure or repair OpenClaw remote access over Tailscale with a directly executable workflow: inspect state, apply the gateway config, enable Tailscale Serve over HTTPS, validate browser access, and handle origin, DNS, or pairing failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiangAgentLabs](https://clawhub.ai/user/JiangAgentLabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure, inspect, and repair OpenClaw gateway access over Tailscale Serve with HTTPS. It guides host-side setup, gateway configuration, Tailscale state checks, validation, and common repair paths for origin, DNS, TLS, and pairing issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes remote-access configuration and handles gateway credentials. <br>
Mitigation: Install only when comfortable granting authority over OpenClaw gateway remote access; treat the gateway token as a secret, avoid passing it on the command line when possible, and restrict config file permissions. <br>
Risk: Diagnostic output can include sensitive hostnames, tokens, device IDs, or pairing details. <br>
Mitigation: Review and redact diagnostic output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JiangAgentLabs/openclaw-tailscale-remote-access) <br>
- [GitHub repository](https://github.com/JiangAgentLabs/openclaw-tailscale-remote-access) <br>
- [Remote Setup](references/remote-setup.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose host commands and configuration changes for OpenClaw, Tailscale, and systemd; users should review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata, SKILL.md metadata.openclaw, CHANGELOG released 2026-03-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
