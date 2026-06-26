## Description: <br>
Manage MikroTik RouterOS devices via API to view status, firewall rules, network configuration, logs, users, backups, traffic details, and execute custom RouterOS commands across one or more devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drodecker](https://clawhub.ai/user/drodecker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and infrastructure engineers use this skill to inspect and administer MikroTik RouterOS devices from an agent workflow, including status checks, firewall and network review, user and service inspection, backups, scans, and custom RouterOS commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad router administration and credential-handling authority. <br>
Mitigation: Use a least-privilege RouterOS account, operate only on authorized devices, and require explicit human approval before custom commands, backups, cleanup, reboot, shutdown, or configuration changes. <br>
Risk: Router credentials may be exposed through CLI password arguments or plaintext workspace notes. <br>
Mitigation: Avoid CLI password arguments and plaintext TOOLS.md secrets; prefer environment variables or a managed secret flow and rotate temporary credentials after use. <br>
Risk: Network scans can generate discovery traffic and may trigger monitoring alerts. <br>
Mitigation: Run scans only on networks where scanning is approved, preferably in a trusted or test segment, and document the scope before execution. <br>
Risk: RouterOS API access may use cleartext transport unless a TLS-capable path is configured. <br>
Mitigation: Prefer a trusted network or TLS-capable client configuration when connecting to RouterOS API services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drodecker/mikrotik-routeros) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries with RouterOS command output and optional inline shell or RouterOS command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live device status, firewall and network configuration summaries, scan results, backup guidance, or custom command results depending on the requested RouterOS operation.] <br>

## Skill Version(s): <br>
2026.3.30 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
