## Description: <br>
Delegates PREQSTATION coding tasks to Claude Code, Codex CLI, or Gemini CLI with PTY-safe worktree execution, background monitoring, and project mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonim1](https://clawhub.ai/user/sonim1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate PREQSTATION-related coding, refactoring, and review work to local coding-agent CLIs while keeping execution in mapped git worktrees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch local coding agents with sandbox and approval checks disabled. <br>
Mitigation: Use it only in trusted repositories and review the planned command, worktree path, and engine before execution. <br>
Risk: Broad `preq` and `preqstation` triggers can unintentionally activate a powerful delegation flow. <br>
Mitigation: Use explicit, scoped requests and confirm ambiguous task intent before launching an engine. <br>
Risk: MEMORY.md stores reusable local workspace paths. <br>
Mitigation: Keep MEMORY.md private and review mapping changes before using them for task execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sonim1/preqstation-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a mapped project workspace, git, and at least one available local engine binary: claude, codex, or gemini.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
