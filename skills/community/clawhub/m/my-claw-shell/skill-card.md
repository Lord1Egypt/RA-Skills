## Description: <br>
Runs shell commands inside a dedicated tmux session named claw and returns captured terminal output to the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biosaylom](https://clawhub.ai/user/biosaylom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when they intentionally want an agent to run local shell commands in a persistent tmux session and read back terminal output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad local terminal access under the local user account. <br>
Mitigation: Install only when terminal access is intended, preferably in a disposable workspace, VM, or container. <br>
Risk: The built-in dangerous-command check is limited and should not be treated as a meaningful safety boundary. <br>
Mitigation: Review every command before use and require explicit user approval for destructive or privileged operations. <br>
Risk: Terminal session history can expose secrets or sensitive working context. <br>
Mitigation: Avoid entering secrets in the tmux session and clear or isolate session state when handling sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biosaylom/my-claw-shell) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [JSON object containing the submitted command or an error plus captured terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a persistent tmux session named claw and may return recent pane history rather than only the command's direct stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
