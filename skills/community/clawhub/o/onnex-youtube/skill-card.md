## Description: <br>
YouTube transcripts, 4K downloads, and video exploration. Onnex-owned fork of youtube-ultimate. Security reviewed before install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mrtlearns](https://clawhub.ai/user/Mrtlearns) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, media researchers, and agents use this skill to retrieve YouTube transcripts, search and inspect videos, channels, comments, playlists, and download video or audio locally when permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags under-disclosed Google account access beyond public video lookup, including subscriptions, playlists, liked videos, and channel data. <br>
Mitigation: Review before installing, use only if that account access is acceptable, and prefer a version with narrower documented read-only scopes. <br>
Risk: The skill saves OAuth tokens locally for authenticated YouTube API commands. <br>
Mitigation: Protect the local token directory, avoid shared machines, and delete local tokens or revoke Google access when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mrtlearns/onnex-youtube) <br>
- [YouTube OAuth scope: readonly](https://www.googleapis.com/auth/youtube.readonly) <br>
- [YouTube OAuth scope: youtube](https://www.googleapis.com/auth/youtube) <br>
- [YouTube OAuth scope: force-ssl](https://www.googleapis.com/auth/youtube.force-ssl) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files] <br>
**Output Format:** [CLI text or JSON responses; downloaded media files for download commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python 3.10 or newer is required. Account-backed YouTube API commands require local Google OAuth credentials and saved tokens; download commands require yt-dlp.] <br>

## Skill Version(s): <br>
4.2.2 (source: frontmatter, _meta.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
