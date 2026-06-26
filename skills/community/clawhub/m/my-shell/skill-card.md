## Description: <br>
Runs shell commands inside a dedicated tmux session named claw, captures output, and prompts before executing potentially destructive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IdIeNet](https://clawhub.ai/user/IdIeNet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run local shell commands in a dedicated tmux session and inspect the captured output. It is intended for controlled environments where agent-driven shell access is explicitly desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent local shell-control capability. <br>
Mitigation: Install only in a disposable or tightly controlled environment where agent shell access is intentional. <br>
Risk: The denylist-based command checks are weak and should not be treated as a safety boundary. <br>
Mitigation: Require human review for sensitive commands and rely on host-level sandboxing, least privilege, and environment isolation. <br>
Risk: The package includes malformed metadata that can write into local OpenClaw skill metadata. <br>
Mitigation: Remove or fix the malformed metadata behavior before trusting or deploying the package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IdIeNet/my-shell) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/IdIeNet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [JSON object containing the submitted command and captured tmux pane output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local tmux environment and uses only the tmux session named claw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-03-07T12:42:44Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
