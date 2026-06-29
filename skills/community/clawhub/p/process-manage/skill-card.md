## Description: <br>
Provides process management commands for listing, finding, inspecting, and terminating local system processes across Windows, Linux, and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxin1044](https://clawhub.ai/user/moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local processes, search by name, retrieve details by PID, and terminate specified processes during troubleshooting or environment cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminating a process can close applications or lose unsaved work, especially when force is true. <br>
Mitigation: Confirm the target PID or process name first, prefer graceful termination, and reserve forceful termination for processes that do not respond. <br>
Risk: Killing by name can affect multiple matching processes when the name is broad. <br>
Mitigation: Use find or info before kill_name, narrow the process name, and terminate by explicit PID when precision matters. <br>
Risk: Terminating system-critical processes can destabilize the host. <br>
Mitigation: Respect the skill's protected-process safeguards and avoid elevated execution unless it is necessary for the user's intended task. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text process reports and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts JSON parameters for action, pid, name, sort, limit, and force.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
