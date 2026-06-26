## Description: <br>
Nexus Safe provides local system health monitoring and policy-controlled Docker/PM2 service recovery without runtime network calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Nexus Safe to inspect local CPU, memory, disk, Docker, and PM2 health, retrieve recent service logs, and perform allowlisted service restarts when policy permits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local service status and logs and may restart Docker or PM2 services when configured. <br>
Mitigation: Install only where local service inspection and recovery are intended, keep restart controls enabled, and restrict allowed Docker and PM2 service lists to the minimum required services. <br>
Risk: Overly broad service permissions could let an agent restart services outside the intended recovery scope. <br>
Mitigation: Use narrow allowlists, keep restart rate limits enabled, and avoid granting broader system privileges than the monitored services require. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrnsmh/nexus-safe) <br>
- [Publisher profile](https://clawhub.ai/user/mrnsmh) <br>
- [Artifact README](artifact/README.md) <br>
- [Agent decision framework](artifact/AGENT_BRAIN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local service logs and write local audit state under ~/.nexus-safe when used.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
