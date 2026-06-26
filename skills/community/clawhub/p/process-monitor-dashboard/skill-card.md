## Description: <br>
Monitor system processes, resource usage, and performance metrics with real-time terminal dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local CPU, memory, disk, network, and process activity from a terminal, including one-time JSON snapshots for scripting and integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal and JSON output may reveal local users, running applications, service names, PIDs, and system layout. <br>
Mitigation: Keep exports local, avoid sharing monitoring output publicly, and install psutil from a trusted package source. <br>


## Reference(s): <br>
- [Process Monitor Dashboard README](README.md) <br>
- [Process Monitor Dashboard on ClawHub](https://clawhub.ai/Derick001/process-monitor-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands return terminal text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local system metrics only; dashboard refresh interval is configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
