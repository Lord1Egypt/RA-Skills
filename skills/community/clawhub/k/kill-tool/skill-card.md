## Description: <br>
Terminate processes by sending signals. Use for stopping unresponsive programs, managing background tasks, and process lifecycle control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to terminate local processes by PID, including graceful shutdown of unresponsive programs and forceful termination when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminating the wrong local process can interrupt work or lose unsaved state, especially when SIGKILL is used. <br>
Mitigation: Confirm the PID and process name before execution, prefer graceful termination first, and reserve SIGKILL for unresponsive processes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/kill-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local process IDs and may send SIGTERM or SIGKILL.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
