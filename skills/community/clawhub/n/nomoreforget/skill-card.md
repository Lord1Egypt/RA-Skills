## Description:

NoMoreForget helps OpenClaw users configure Memory Flush, organize memory files, and run diagnostic, backup, restore, and optimization scripts to reduce memory loss, token waste, and search failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steventsang18](https://clawhub.ai/user/steventsang18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up Memory Flush, organize long-term and daily memory files, and diagnose, back up, restore, or optimize memory state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: restore_memory.sh can overwrite persistent OpenClaw memory files and server security evidence flags unsafe command handling.

Mitigation: Avoid restore_memory.sh until input validation is fixed; if recovery is required, review the script and restore target first, then run it only from a trusted local copy.

Risk: The install and restore flows can modify ~/.openclaw configuration and workspace memory files.

Mitigation: Back up ~/.openclaw before installation or restore, and verify openclaw.json, MEMORY.md, and daily logs after changes.

Risk: Enabling Memory Flush can save selected conversation details into persistent OpenClaw memory files across sessions.

Mitigation: Do not store secrets or private data in memory files, and periodically review MEMORY.md and daily logs for sensitive content.

## Reference(s):

- [NoMoreForget ClawHub page](https://clawhub.ai/steventsang18/skills/nomoreforget)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw memory architecture](references/architecture.md)
- [OpenClaw memory plugin ecosystem](references/plugins.md)
- [OpenClaw memory troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local OpenClaw configuration and memory-file maintenance actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
