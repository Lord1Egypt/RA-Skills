## Description: <br>
Generate copy-paste bash scripts for Ralph Wiggum/AI agent loops (Codex, Claude Code, OpenCode, Goose). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Endogen](https://clawhub.ai/user/Endogen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to set up monitored AI coding loops that alternate between planning and building, run tests or lint checks, and notify OpenClaw when work completes, blocks, or needs human input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The loop can repeatedly run autonomous coding agents, commands, notifications, and persistent services with limited user gating. <br>
Mitigation: Install only in isolated repositories or disposable sandboxes, review generated work before reuse, and keep secrets out of prompts and logs. <br>
Risk: Auto-approve or permission-skip flags can grant broad write or command execution authority to an agent. <br>
Mitigation: Review and override RALPH_FLAGS before use, and avoid permission-skip modes unless the execution environment is intentionally isolated. <br>
Risk: RALPH_TEST executes user-provided shell content and host setup snippets can alter system-level persistence. <br>
Mitigation: Treat RALPH_TEST as arbitrary shell code and do not run systemd or /etc/fstab snippets without understanding the host-level effects. <br>


## Reference(s): <br>
- [Monitored Ralph Loop on ClawHub](https://clawhub.ai/Endogen/monitored-ralph-loop) <br>
- [Ralph pattern](https://ghuntley.com/ralph/) <br>
- [snarktank/ralph](https://github.com/snarktank/ralph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, prompt templates, agent loop scripts, notification file conventions, and operational safety guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
