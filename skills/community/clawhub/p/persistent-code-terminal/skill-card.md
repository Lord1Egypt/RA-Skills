## Description:

Persistent per-project coding terminal (tmux). Run Codex CLI (codex exec) inside a stable session; mobile/SSH friendly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinzhq](https://clawhub.ai/user/justinzhq)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to run coding commands and Codex CLI work inside persistent tmux sessions, preserving output and shell state across SSH or mobile reconnects. It supports one-project and multi-project coding workflows with status, summary, JSON output, and optional auto-routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Codex with write authority and retry coding tasks automatically.

Mitigation: Install it only in repositories where automated code edits are acceptable, keep auto routing disabled unless intentionally enabled, and review diffs before commit or push.

Risk: Persistent terminal output and state files may retain sensitive command or session data.

Mitigation: Avoid putting secrets in prompts or shell commands, and add `.pct-state.json` and `.pct-routing.log` to gitignore or clean them regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justinzhq/skills/persistent-code-terminal)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on macOS or Linux; Codex CLI is optional for Codex-driven workflows.]

## Skill Version(s):

1.2.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
