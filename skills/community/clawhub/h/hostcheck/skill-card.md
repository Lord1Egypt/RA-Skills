## Description: <br>
Hostcheck provides a free host health check for OpenClaw deployments, covering system status, updates, security settings, and recommendations without requiring paid tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwtomekk-bit](https://clawhub.ai/user/bwtomekk-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for read-only host health and security posture checks on OpenClaw deployments, including update status, SSH and firewall posture, backups, service health, and actionable maintenance recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested sudo, package upgrade, firewall, or installation commands could affect host configuration if executed without review. <br>
Mitigation: Treat those commands as manual administrator actions and approve them only after confirming they fit the operating system and maintenance window. <br>
Risk: The skill may inspect local host health and security posture. <br>
Mitigation: Install it only when an agent should review local system status, security settings, backups, and OpenClaw service health. <br>


## Reference(s): <br>
- [Hostcheck ClawHub skill page](https://clawhub.ai/bwtomekk-bit/hostcheck) <br>
- [bwtomekk-bit publisher profile](https://clawhub.ai/user/bwtomekk-bit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status report with inline shell commands and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; recommends manual approval before any host changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
