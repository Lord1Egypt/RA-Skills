## Description: <br>
Delegate coding tasks to Codex, Claude Code, OpenCode, or Pi agents through PTY-enabled bash sessions for building features, reviewing PRs, refactoring, and longer iterative coding work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate larger coding, refactoring, and pull request review tasks to local coding-agent CLIs while keeping work scoped to an explicit project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous coding-agent CLIs may modify projects, create branches, push changes, or open pull requests using the user's existing accounts. <br>
Mitigation: Run agents in sandboxed or temporary worktrees, keep task scope narrow, review changes before commits, and require explicit approval before any push, PR, or OpenClaw event command. <br>
Risk: No-sandbox or auto-approval modes can reduce checkpoints around local file changes. <br>
Mitigation: Avoid no-sandbox modes unless the workspace is disposable, set timeouts, and monitor background sessions before accepting generated changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rmbell09-lang/lucky-coding-agent) <br>
- [Publisher profile](https://clawhub.ai/user/rmbell09-lang) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a bash tool with PTY support and one of the configured coding-agent CLIs: claude, codex, opencode, or pi.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
