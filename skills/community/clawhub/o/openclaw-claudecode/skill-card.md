## Description: <br>
Controls Claude Code through tmux sessions to start development sessions, send development commands, monitor progress, and handle prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanzhidongyzby](https://clawhub.ai/user/fanzhidongyzby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate long-running development work to Claude Code in a detached tmux session, then monitor output and interact with the session when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to drive Claude Code in a detached tmux session with broad unattended coding authority. <br>
Mitigation: Run it only for intended development tasks, prefer normal Claude Code permission checks over dangerous skip-permissions mode, and review session output and code changes before use. <br>
Risk: Setup guidance can involve privileged package installation, user creation, and external installer commands. <br>
Mitigation: Review setup commands before execution, avoid curl-pipe-shell installers unless verified, and use an existing low-privilege account where possible. <br>
Risk: Claude Code credentials or API keys may be exposed through tmux panes, captures, logs, or session history. <br>
Mitigation: Protect ANTHROPIC_API_KEY and login state, limit access to tmux sessions, avoid capturing secrets, and clean up sessions when work is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanzhidongyzby/openclaw-claudecode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tmux session commands, Claude Code setup checks, monitoring commands, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
