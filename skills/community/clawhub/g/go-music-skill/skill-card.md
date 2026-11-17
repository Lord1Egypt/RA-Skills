## Description:

Search songs, download playable audio, fetch lyrics, parse music share links, configure platform cookies, and switch music sources through a local go-music-api backend on Linux, macOS, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavin](https://clawhub.ai/user/scavin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and run a local music backend, search for tracks, download playable audio, fetch lyrics, and configure platform cookies for login-required music sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs a third-party backend executable as a local service.

Mitigation: Install only after reviewing the backend source and release provenance, and monitor or stop the local service when it is no longer needed.

Risk: The skill may process music-service cookies for login-required tracks.

Mitigation: Use the minimum required cookie values, avoid printing full cookies in chat or logs, and rotate or revoke cookies after use when appropriate.

Risk: The skill writes runtime state, cache files, downloaded media, logs, PID files, and port files under ~/.openclaw.

Mitigation: Review and clean the ~/.openclaw/music and ~/.openclaw/media directories according to local retention and privacy expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavin/skills/go-music-skill)
- [Music Skill repository](https://github.com/scavin/Music-Skill)
- [go-music-api releases API](https://api.github.com/repos/guohuiyuan/go-music-api/releases/latest)
- [Windows workflow](artifact/docs/windows.md)
- [Cookie configuration](artifact/docs/cookies.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio files and metadata updates when the bundled scripts are executed.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
