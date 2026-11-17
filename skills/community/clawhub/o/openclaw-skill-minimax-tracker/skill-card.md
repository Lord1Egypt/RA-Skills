## Description:

Track and monitor MiniMax API usage with real-time progress bars, automatic resets, and scheduled reminders for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaotucodes](https://clawhub.ai/user/qiaotucodes)

### License/Terms of Use:

MIT License

## Use Case:

Developers and OpenClaw agent operators use this skill to record MiniMax prompt usage, check remaining quota, and configure periodic reminders around usage resets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tracker creates or updates local usage state at ~/.openclaw/workspace/minimax_usage_data.json.

Mitigation: Run it only in a workspace where local usage tracking is expected and review the file path before using the add command.

Risk: Reminder configuration can trigger periodic status checks.

Mitigation: Configure the schedule only when periodic MiniMax usage reminders are desired.

Risk: Installing from a repository without verification can introduce unreviewed code changes.

Mitigation: Prefer a reviewed release, pinned commit hash, or checksum-verified copy before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaotucodes/skills/openclaw-skill-minimax-tracker)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [MiniMax platform](https://platform.minimaxi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, JSON configuration examples, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script can print compact or detailed usage status and can update a local JSON usage file.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
