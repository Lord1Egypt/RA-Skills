## Description: <br>
Manages context overflow by handing off to a fresh subagent at 80% usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve progress during long-running work by checkpointing session state and delegating continuation to a fresh subagent when context usage is high. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill preserves dangerous or unattended execution modes across subagents without a fresh user confirmation step. <br>
Mitigation: Prefer interactive mode, inspect .claude/session-state.md before handoff, and pre-authorize only bounded work before using unattended or dangerous modes. <br>
Risk: Continuation across context resets can carry forward sensitive or high-impact tasks. <br>
Mitigation: Avoid using the skill for tasks involving destructive changes, credentials, external posting, or other sensitive side effects unless that scope has been explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-clear-context) <br>
- [Conserve plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks and session-state templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update .claude/session-state.md, or a path set with CONSERVE_SESSION_STATE_PATH, and may delegate continuation to a fresh subagent when supported.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
