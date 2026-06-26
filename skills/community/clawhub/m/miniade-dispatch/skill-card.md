## Description: <br>
Launch non-blocking Claude Code headless tasks from slash command dispatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edxi](https://clawhub.ai/user/edxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to start asynchronous Claude Code jobs against local project workspaces when a task can run in the background and report a run id, result directory, and log path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Claude Code against local repositories in background processes or detached tmux sessions. <br>
Mitigation: Install only in trusted workspaces, restrict project names to known repository slugs, and check for remaining nohup or tmux Claude sessions after use. <br>
Risk: Some modes can automatically approve Claude Code security prompts, including bypassPermissions flows. <br>
Mitigation: Avoid bypassPermissions and use the most restrictive permission mode compatible with the task. <br>
Risk: Prompts, logs, and task output may be written to local result and launch log directories. <br>
Mitigation: Keep result and log directories private and avoid putting secrets or sensitive data in prompts. <br>


## Reference(s): <br>
- [Claude Code headless mode documentation](https://code.claude.com/docs/en/headless) <br>
- [Claude Code Agent Teams documentation](https://code.claude.com/docs/en/agent-teams) <br>
- [ClawHub skill page](https://clawhub.ai/edxi/miniade-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text launch summary with command-line configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns run identifiers, result paths, and log paths for background Claude Code jobs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
