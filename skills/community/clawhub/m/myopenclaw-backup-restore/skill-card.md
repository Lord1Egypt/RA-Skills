## Description: <br>
Cross-platform backup and restore for OpenClaw across Windows, macOS, and Linux, with dry-run previews, pre-restore snapshots, credential permission hardening, and browser-based local management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyound87](https://clawhub.ai/user/beyound87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create portable snapshots, migrate OpenClaw state between machines, and recover from data loss. It is intended for environments where the operator can protect backups that contain credentials, sessions, and configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives can contain bot tokens, API keys, session credentials, and other sensitive OpenClaw state. <br>
Mitigation: Treat archives like password vaults: store them securely, transfer them only over encrypted channels, never commit them publicly, and restore only archives you created or fully trust. <br>
Risk: The browser management server handles backup upload, download, and restore workflows over a network-accessible listener. <br>
Mitigation: Keep the server on localhost or a trusted network or tunnel, require a strong token, and prefer environment-based or Authorization-header tokens over URL tokens. <br>
Risk: Restore operations overwrite OpenClaw state and may reintroduce executable scripts, credentials, or stale configuration from an archive. <br>
Mitigation: Run dry-run preview first, keep the automatic pre-restore snapshot, review the archive source, and confirm destructive restores only when the restored state is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beyound87/myopenclaw-backup-restore) <br>
- [OpenClaw Backup - What Gets Saved](references/what-gets-saved.md) <br>
- [MyClaw.ai](https://myclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts create backup archives and restore OpenClaw files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and read/write access to ~/.openclaw; optional local HTTP server listens for browser-based management.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
