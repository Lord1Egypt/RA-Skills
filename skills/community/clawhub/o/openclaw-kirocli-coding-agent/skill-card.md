## Description:

Run Codex CLI, Claude Code, Kiro CLI, OpenCode, or Pi Coding Agent via background process for programmatic control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandysuper](https://clawhub.ai/user/dandysuper)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill in OpenClaw to launch, monitor, and interact with coding-agent CLIs for coding tasks, reviews, planning sessions, and project automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends no-confirmation or unrestricted-tool modes for coding agents.

Mitigation: Prefer confirmation-enabled or allowlisted tool modes, and reserve unrestricted modes for isolated sandboxes.

Risk: Unsandboxed coding-agent execution can modify files, run commands, or affect repositories beyond the intended task.

Mitigation: Run agents in a focused workdir, review changes before commit, push, or pull request actions, and avoid unsandboxed execution on sensitive projects.

Risk: Pipe-to-shell or unpinned global installer patterns can introduce supply-chain risk during prerequisite setup.

Mitigation: Review installer sources, prefer pinned or package-managed installs where available, and avoid pipe-to-shell setup in privileged environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dandysuper/skills/openclaw-kirocli-coding-agent)
- [Kiro CLI](https://kiro.dev/)
- [Kiro CLI Installation](https://kiro.dev/docs/cli/installation)
- [Kiro Custom Agents Configuration Reference](https://kiro.dev/docs/cli/custom-agents/configuration-reference)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PTY for interactive coding-agent CLIs and supports background session monitoring with stdin relay.]

## Skill Version(s):

1.5.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
