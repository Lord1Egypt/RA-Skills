## Description: <br>
Use when user asks about Bridge to local Claude Code CLI - no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cry779](https://clawhub.ai/user/cry779) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create and run local Claude Code tasks for code generation, code review, and data analysis through an existing logged-in Claude Code CLI subscription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge can grant local file read, file edit, and shell-command capability through the user's logged-in Claude Code session. <br>
Mitigation: Run it only in a sandbox or disposable workspace and review generated scripts before execution. <br>
Risk: The release includes old task scripts and results that can reference or modify unrelated local projects. <br>
Mitigation: Review and delete bundled tasks and results before installing or running the skill. <br>
Risk: Prompts and local files may be exposed according to the user's local Claude Code configuration. <br>
Mitigation: Avoid putting secrets or private code in prompts unless the local Claude Code routing and data handling are verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cry779/openclaw-claude-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/cry779) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON task/result files with generated shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Claude Code CLI installation, a logged-in account, and an active subscription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
