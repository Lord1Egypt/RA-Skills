## Description: <br>
Watch and control running processes in real time, including active PIDs, resource spikes, process trees, crash checks, logs, and listening ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and system administrators use ProcMon to inspect local process activity, watch named processes, identify CPU or memory heavy processes, find zombies, inspect process trees, log matching process stats, and view listening ports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local process and listening-port information that may reveal sensitive operational details. <br>
Mitigation: Run it only in environments where the agent is allowed to inspect local process and port state. <br>
Risk: The procmon log command writes local process history under ~/.procmon. <br>
Mitigation: Delete ~/.procmon logs when historical process records are no longer needed. <br>


## Reference(s): <br>
- [Procmon on ClawHub](https://clawhub.ai/bytesagain3/procmon) <br>
- [bytesagain3 publisher profile](https://clawhub.ai/user/bytesagain3) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with command examples and local log file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local process identifiers, command names, resource usage, process states, process trees, listening ports, and log paths under ~/.procmon.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
