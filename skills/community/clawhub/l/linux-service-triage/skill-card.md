## Description: <br>
Diagnoses common Linux service issues using logs, systemd/PM2, file permissions, Nginx reverse proxy checks, and DNS sanity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to triage failing or unreachable Linux services, interpret supplied logs and status output, and plan minimal fixes for systemd, PM2, permissions, Nginx, DNS, and related service issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reloads, restarts, permission changes, and systemd service creation can affect service availability or persistence. <br>
Mitigation: Review proposed commands before execution, require explicit user approval for changes, and prefer validation steps such as nginx -t and port checks before reloads. <br>
Risk: Troubleshooting based on incomplete logs or status output can lead to an incorrect fix plan. <br>
Mitigation: Ask for missing logs, status output, service names, ports, and configuration snippets before recommending changes. <br>


## Reference(s): <br>
- [Linux Service Triage Commands](references/triage-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Structured triage report with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; exact fix commands are provided only when explicitly requested and safe.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
