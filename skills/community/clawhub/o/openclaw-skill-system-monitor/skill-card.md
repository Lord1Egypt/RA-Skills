## Description: <br>
Real-time system metrics monitoring for CPU, memory, disk, network, processes, and system load on macOS and Linux using native CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to inspect local system health, including CPU load, memory use, disk space, network activity, running processes, and load average. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local process and network diagnostics may expose sensitive services, usernames, connection details, or command arguments. <br>
Mitigation: Review diagnostic output before sharing it outside the local troubleshooting context, and redact sensitive process, network, filesystem, and user details. <br>
Risk: The skill runs local diagnostic commands that inspect system state. <br>
Mitigation: Install and use it only when local system monitoring is intended, and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ppopen/openclaw-skill-system-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/ppopen) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [System Stats Script](artifact/scripts/system-stats.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local process, network, filesystem, username, command, and service details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
