## Description: <br>
Preqstation delegates mapped workspace coding tasks to Claude Code, Codex CLI, or Gemini CLI using worktree-first, PTY-based background execution and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonim1](https://clawhub.ai/user/sonim1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Preqstation to route natural-language coding, refactoring, and review tasks to a local coding-agent CLI in a mapped project workspace. It is intended for worktree-scoped execution with background monitoring, not for one-line edits or read-only inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start background code-changing agents with approval and sandbox bypass flags. <br>
Mitigation: Install only for trusted repositories, use it only with intentional local CLI delegation, and inspect worktree diffs before merging or pushing. <br>
Risk: Incorrect project mappings could send coding-agent work to the wrong workspace. <br>
Mitigation: Verify MEMORY.md project mappings and require absolute, resolved project paths before execution. <br>
Risk: Long-running background sessions may continue after the initiating request. <br>
Mitigation: Monitor sessions with poll or log actions and stop background sessions when they are no longer needed. <br>


## Reference(s): <br>
- [Preqstation ClawHub release page](https://clawhub.ai/sonim1/preqstation) <br>
- [Publisher profile: sonim1](https://clawhub.ai/user/sonim1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise status text with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start and monitor background PTY sessions for local Claude, Codex, or Gemini CLI execution.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
