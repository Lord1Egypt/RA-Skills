## Description:

Manage long-running Cursor CLI coding tasks through OpenClaw tools backed by tmux sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzeyu99-web](https://clawhub.ai/user/zhangzeyu99-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to start, monitor, update, and stop persistent Cursor CLI coding tasks from OpenClaw, with tmux sessions preserving long-running work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful Cursor and tmux task control without enough authorization or project scoping.

Mitigation: Use only in a trusted, isolated OpenClaw environment; require authentication for /cursor and restrict allowed project roots before using with valuable repositories or credentials.

Risk: Setup material includes unsafe installation and restore guidance, including curl-to-shell commands and personal backup restore instructions.

Mitigation: Remove personal backup restore instructions and avoid curl-to-shell installers; review setup steps before installation.

Risk: Default trust, force, or shell escaping behavior can increase the impact of malformed input or unintended command execution.

Mitigation: Remove default --trust/--force behavior and fix shell escaping before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangzeyu99-web/skills/openclaw-cursor-agent)
- [Usage guide](docs/usage-guide.md)
- [Plugin README](extensions/openclaw-cursor-agent/README.md)
- [Cursor Agent System README](cursor-agent-system/README.md)
- [Command patterns](extensions/openclaw-cursor-agent/skill/references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with tool-status summaries, command guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session names, task IDs, progress, tmux status, missing dependency names, and follow-up commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
