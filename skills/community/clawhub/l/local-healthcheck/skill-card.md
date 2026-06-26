## Description: <br>
Simple local security check (firewall, updates, ssh status) without external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fedrov2025](https://clawhub.ai/user/fedrov2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and local users use this skill to create a quick macOS or Linux security snapshot covering firewall status, listening ports, available software updates, and SSH daemon state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local health report may reveal sensitive system details such as open ports, firewall state, update status, and SSH daemon status. <br>
Mitigation: Treat the generated report as sensitive and share it only with trusted reviewers or administrators. <br>
Risk: Some checks may request elevated privileges through sudo. <br>
Mitigation: Review each sudo prompt before approving it and run the skill only when a local machine security snapshot is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fedrov2025/local-healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated local report to memory/healthcheck-YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
