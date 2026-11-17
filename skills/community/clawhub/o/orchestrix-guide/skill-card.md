## Description:

Orchestrix Guide provides an OpenClaw operating guide for coordinating Orchestrix agents through Claude Code and tmux across planning, development, testing, bug-fix, iteration, brownfield, and change-management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorayo](https://clawhub.ai/user/dorayo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to guide OpenClaw-driven Orchestrix workflows that create planning documents, coordinate multi-agent development handoffs, run epic smoke tests, and handle bug-fix or change-management paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can bypass normal Claude Code permission checks during code-changing tasks.

Mitigation: Keep normal Claude Code approvals enabled and avoid the --dangerously-skip-permissions alias.

Risk: The workflow can auto-accept folder trust and approval prompts in repositories that have not been inspected.

Mitigation: Use the skill only in an isolated project or container and inspect repositories before trusting them.

Risk: tmux automation can send commands to the wrong session, window, or project directory if configured incorrectly.

Mitigation: Verify the target session, window, and project path before running commands, and review generated file changes before committing.

## Reference(s):

- [Orchestrix MCP Homepage](https://orchestrix-mcp.youlidao.ai)
- [Claude Code Download](https://claude.ai/download)
- [ClawHub Skill Page](https://clawhub.ai/dorayo/skills/orchestrix-guide)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dorayo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets, workflow diagrams, command tables, and operational checklists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and guidance are intended for macOS or Linux environments with Claude Code, tmux, git, and optional jq.]

## Skill Version(s):

3.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
