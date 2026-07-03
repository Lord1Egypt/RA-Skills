## Description: <br>
It Ops Toolkit helps agents choose and run Python scripts for network diagnostics, system monitoring, service checks, troubleshooting, and utility tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[microsnow](https://clawhub.ai/user/microsnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT operations engineers and developers use this skill to run authorized checks for connectivity, host health, service status, logs, performance issues, camera streams, and common utility conversions. It is intended to help select commands, execute the relevant local scripts, and summarize the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actively probe networks, cameras, remote SSH hosts, logs, and services. <br>
Mitigation: Use it only on systems you own or manage, review proposed commands before execution, and avoid placing real passwords in command lines or RTSP URLs. <br>
Risk: Remote SSH behavior is not fully safeguarded for production infrastructure. <br>
Mitigation: Review or patch SSH host-key handling before production use and prefer key-based authentication over password arguments. <br>
Risk: IP lookup functionality contacts a third-party service. <br>
Mitigation: Avoid submitting sensitive IP addresses unless that external lookup is approved for the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/microsnow/it-ops-toolkit) <br>
- [Server-Resolved GitHub Source](https://github.com/microsnow/it-ops-toolkit.git) <br>
- [Command Reference](references/commands_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local Python scripts that perform network, system, SSH, Docker, database, log, and RTSP checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
