## Description: <br>
Hardens an OpenClaw Linux server with SSH key-only authentication, UFW firewall rules, fail2ban protection, credential permissions, and an optional gateway service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when setting up or auditing an OpenClaw Linux host that needs SSH, firewall, brute-force protection, credential permission, and optional gateway service guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH and firewall changes can lock administrators out or disrupt access if applied without preparation. <br>
Mitigation: Verify key-based SSH access, review each command before execution, and keep rollback access before disabling password auth or enabling restrictive firewall rules. <br>
Risk: The optional OpenClaw gateway service creates a persistent boot-time systemd service that runs as root. <br>
Mitigation: Review the systemd unit before enabling it, avoid running the gateway as root when possible, and confirm boot-time enablement is intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ppiankov/host-hardening) <br>
- [Agent-Native CLI Convention](https://ancc.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review and approval before executing host-level commands.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
