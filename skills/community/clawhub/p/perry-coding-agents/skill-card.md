## Description: <br>
Dispatch coding tasks to OpenCode or Claude Code on Perry workspaces for development work, PR reviews, or coding tasks that need an isolated environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gricha](https://clawhub.ai/user/gricha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to delegate coding work, PR review follow-up, and CI-fix tasks to OpenCode or Claude Code running on Perry workspaces while tracking each dispatched task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates coding work to remote agents with broad ability to run commands and change repositories. <br>
Mitigation: Review each dispatch request, use it only with intended Perry workspaces, and avoid enabling it in sensitive repositories unless remote background tasks creating branches or PRs are acceptable. <br>
Risk: The documented dispatch flow relies on SSH connections and remote background execution. <br>
Mitigation: Use trusted host aliases or pinned SSH host keys where possible, confirm workspace IPs before dispatch, and inspect generated branches, PRs, and CI results before merging. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SSH dispatch patterns and task-tracking guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
