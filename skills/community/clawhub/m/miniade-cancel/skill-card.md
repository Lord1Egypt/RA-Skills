## Description: <br>
Cancel an active interactive dispatch or ralph-loop run by run ID from the `/cancel` slash command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edxi](https://clawhub.ai/user/edxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators using OpenClaw dispatch use this skill to stop an active interactive run when it should be cancelled immediately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Path-like run IDs may reach a local tmux session and run metadata without enough containment checks. <br>
Mitigation: Validate project and run ID characters, reject `..` and unexpected path segments, canonicalize the target directory, and verify it remains under the configured results base before sending tmux commands. <br>
Risk: The cancel action can kill local tmux sessions and rewrite run metadata. <br>
Mitigation: Install and run only in environments where the operator understands and accepts those local side effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edxi/miniade-cancel) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text] <br>
**Output Format:** [Shell command execution with a plain-text status or error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one run ID argument; supports project/run ID form when needed to disambiguate.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
