## Description:

Package and reuse the MeowMusicServer-patched YouTube fallback workflow: Windows Chrome cookie export and sync to a server, server-side yt-dlp, yt-dlp-ejs, and ffmpeg setup, old-source-first YouTube fallback, and MV-to-MP3 extraction and caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe12801](https://clawhub.ai/user/joe12801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or debug a YouTube fallback path for MeowMusicServer or similar music services while preserving legacy music sources first. It also supports refreshing browser cookies from a Windows profile, preparing a Linux server runtime, and producing cached MP3 files for stable playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles browser session cookies and admin bearer tokens.

Mitigation: Use a dedicated low-privilege browser profile or account, keep tokens in environment variables, avoid committing secrets, and restrict server-side cookie files to minimal file permissions.

Risk: The cookie update API can expose sensitive session material if deployed without strong transport and access controls.

Mitigation: Use HTTPS for non-loopback endpoints, require strong authentication on the update endpoint, and keep cookie retention short.

Risk: Runtime setup installs and updates external tools used for media download and conversion.

Mitigation: Install dependencies in an isolated environment, pin dependency versions for production, and review generated shell commands before running them on a server.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joe12801/skills/meowmusic-youtube-mp3)
- [Cookie API and Windows Sync](references/cookie-api-and-sync.md)
- [Known-Good Context](references/known-good-context.md)
- [MeowMusic Integration Notes](references/meowmusic-integration.md)
- [Server Runtime Notes](references/server-runtime-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose server patches, cookie-sync commands, runtime setup steps, and MP3 caching configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
