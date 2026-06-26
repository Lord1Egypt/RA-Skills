## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and control existing tmux sessions for interactive command-line tools, including capturing pane output, sending keystrokes, and checking long-running session status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect terminal history and live pane output, which may expose sensitive command output or prompts. <br>
Mitigation: Verify the target session before capture and collect only the minimum pane output needed for the task. <br>
Risk: The skill can type into live tmux sessions and approve interactive prompts. <br>
Mitigation: Require explicit confirmation before sending Enter, control keys, approval responses, or other input that changes program state. <br>
Risk: Session-management commands can rename, create, or kill tmux sessions. <br>
Mitigation: Confirm the exact target session and require approval before running session-management commands such as kill-session, rename-session, or new-session. <br>


## Reference(s): <br>
- [Lucky Tmux Controller on ClawHub](https://clawhub.ai/rmbell09-lang/lucky-tmux) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on Darwin or Linux and may inspect or control live terminal sessions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
