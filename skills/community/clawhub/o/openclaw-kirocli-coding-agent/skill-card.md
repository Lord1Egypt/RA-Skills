## Description: <br>
Run Codex CLI, Claude Code, Kiro CLI, OpenCode, or Pi Coding Agent via background process for programmatic control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandysuper](https://clawhub.ai/user/dandysuper) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to launch, monitor, and interact with coding-agent CLIs from OpenClaw while keeping each agent focused on a chosen working directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous coding agents may make broad local code or shell changes when run with no-approval or trust-all-tools modes. <br>
Mitigation: Use isolated workspaces, prefer scoped tool trust or sandboxed modes, and review file changes before commits, pushes, or deployment. <br>
Risk: Running coding agents near secrets or production repositories can expose sensitive files or modify critical assets. <br>
Mitigation: Keep secrets and production repositories outside the working directory unless strong containment and access controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandysuper/openclaw-kirocli-coding-agent) <br>
- [Kiro CLI installation](https://kiro.dev/docs/cli/installation) <br>
- [Kiro CLI custom agents configuration](https://kiro.dev/docs/cli/custom-agents/configuration-reference) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one supported coding-agent binary: claude, codex, opencode, pi, or kiro-cli.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
