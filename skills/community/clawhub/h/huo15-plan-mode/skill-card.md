## Description: <br>
Huo15 Plan Mode provides advisory scripts and guidance for classifying risky shell operations and generating confirmation prompts before potentially destructive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators can use this skill as an advisory Plan Mode helper to identify higher-risk commands, produce confirmation text, and document a confirmation workflow for OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the skill for a complete safety boundary for destructive commands. <br>
Mitigation: Treat it as advisory only, and require platform- or agent-level confirmation controls before executing destructive commands in real workspaces. <br>
Risk: The setup flow modifies workspace heartbeat content and creates activity log files. <br>
Mitigation: Review the workspace file changes before installation and test the setup in a disposable workspace first. <br>
Risk: The integration wrapper includes eval-based command execution paths. <br>
Mitigation: Do not source the integration wrapper around untrusted command strings, and review commands explicitly before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-plan-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory risk checks and confirmation prompt text; it does not fully implement reply handling or gated command execution by itself.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
