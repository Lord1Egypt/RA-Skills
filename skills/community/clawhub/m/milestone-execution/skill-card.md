## Description: <br>
Milestone Execution helps users break complex work into controlled milestones that run in an independent agent work session, pause after each stage, and wait for confirmation before continuing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siesta-0402](https://clawhub.ai/user/siesta-0402) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decompose large coding, review, or build tasks into milestone-by-milestone work sessions with explicit user approval between stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to spawn work sessions and modify files in the current workspace. <br>
Mitigation: Run it only in a controlled project directory, review milestone reports before continuing, and inspect file changes between stages. <br>
Risk: An existing .milestone-state.json can affect recovery or continuation behavior. <br>
Mitigation: Check for an existing .milestone-state.json before starting and clear or archive stale state when beginning unrelated work. <br>
Risk: The documented parallel milestone flow has unclear executor and session ownership behavior in the release evidence. <br>
Mitigation: Avoid parallel milestones until the package includes the documented executor and clearer session/state ownership rules. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/siesta-0402/milestone-execution) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, text] <br>
**Output Format:** [Markdown progress reports with inline shell commands and JSON state/status data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads .milestone-state.json in the current workspace and may spawn or resume agent work sessions.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter and README list 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
