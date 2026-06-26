## Description: <br>
Port Process helps agents find and manage system processes by port, including identifying port owners, listing listening ports, and terminating selected processes on macOS and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill during local development, debugging, and automation to identify processes occupying ports and safely free ports before starting services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process termination commands can stop the wrong local process or interrupt stateful work if the PID and process name are not reviewed first. <br>
Mitigation: Inspect the PID and command with the find or dry-run workflow before terminating, and avoid applying kill commands to critical or unfamiliar processes. <br>
Risk: Force-kill behavior can prevent graceful shutdown and may cause data loss for services with unsaved state. <br>
Mitigation: Prefer graceful termination first, use the safe mode when available, and reserve SIGKILL or kill -9 for cases where the process can be stopped. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/wang-junjian/port-process) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local process inspection and port cleanup workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
