## Description: <br>
Dispatches long-running coding tasks to Claude Code CLI with automatic callback notifications to Feishu or WeCom when complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xclipse](https://clawhub.ai/user/xclipse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to hand off substantial project creation, feature work, refactoring, and codebase improvement tasks to Claude Code while receiving Feishu or WeCom completion notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can dispatch unattended coding work that may modify files without interactive review. <br>
Mitigation: Require explicit approval before each dispatch and prefer a reviewed permission mode such as acceptEdits for sensitive repositories. <br>
Risk: Completion details may be sent to configured Feishu or WeCom targets. <br>
Mitigation: Confirm destination IDs belong to channels or users the operator controls before dispatching work. <br>
Risk: The workflow depends on local dispatcher scripts and notification hooks outside the skill artifact. <br>
Mitigation: Install and use the skill only in environments where the local dispatcher and notification hooks are trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xclipse/openclaw-claude-dispatcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task descriptions, working directories, notification channel choices, dispatch commands, and confirmation text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
