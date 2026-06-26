## Description: <br>
Create monitors for anything. User defines what to check, skill handles scheduling and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to define recurring health, availability, certificate, process, disk, port, and custom checks, then receive alerts when monitor state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring user-defined shell commands may run with the agent's local privileges. <br>
Mitigation: Review every custom command before enabling it, prefer built-in checks where possible, and only grant additional access such as SSH or Docker when necessary. <br>
Risk: Alert messages, monitor names, logs, or webhook destinations may expose sensitive internal hostnames or secrets. <br>
Mitigation: Use trusted webhook destinations and avoid putting secrets or sensitive internal identifiers in monitor names, logs, or alert payloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/monitor) <br>
- [Monitor Templates](templates.md) <br>
- [Alert Configuration](alerts.md) <br>
- [Monitor Analysis Patterns](insights.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create monitor definitions, alert configuration, and log summaries under ~/monitor/.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
