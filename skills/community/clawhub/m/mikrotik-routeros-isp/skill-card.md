## Description: <br>
Assists with MikroTik RouterOS device and VSOL GPON OLT administration over SSH, RouterOS API, and REST API for ISP infrastructure workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charllesvale](https://clawhub.ai/user/charllesvale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network operators, ISP engineers, and automation-focused developers use this skill to inspect, configure, back up, and troubleshoot MikroTik RouterOS devices and VSOL GPON OLTs. It is aimed at production network administration workflows that require careful review before applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands and scripts can change live router, firewall, NAT, PPPoE, routing, OLT, or failover configuration on production networks. <br>
Mitigation: Use least-privilege management accounts, review each proposed command before execution, export or back up configuration first, and verify state after changes. <br>
Risk: Device credentials and management endpoints may be exposed if passwords are stored in plaintext or API sessions are not TLS-validated. <br>
Mitigation: Prefer SSH keys and TLS-validated API-SSL, keep passwords out of TOOLS.md and scripts, and provide secrets through controlled environment variables or secret stores. <br>
Risk: Third-party notifications, backup uploads, and auto-updated RouterOS scripts can disclose operational data or introduce unreviewed code. <br>
Mitigation: Audit external scripts before use, disable or pin auto-updates, self-host reviewed copies where practical, and use external notification or upload integrations only with appropriate retention and access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charllesvale/mikrotik-routeros-isp) <br>
- [RouterOS Command Reference](references/routeros-commands.md) <br>
- [RouterOS API + REST API Reference](references/routeros-api.md) <br>
- [Failover Actions + Notificacoes](references/failover-notifications.md) <br>
- [eworm-de/routeros-scripts Reference](references/eworm-scripts.md) <br>
- [VSOL GPON OLT SSH Reference](references/vsol-olt.md) <br>
- [ISP Stack Reference](references/isp-stack.md) <br>
- [MikroTik RouterOS documentation](https://help.mikrotik.com/docs) <br>
- [eworm RouterOS scripts documentation](https://rsc.eworm.de/main/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline RouterOS, bash, Python, curl, and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational warnings, backup steps, validation commands, and API request examples.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
