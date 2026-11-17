## Description:

Apple Music integration via AppleScript (macOS) or MusicKit API

This skill is ready for commercial/non-commercial use.

## Publisher:

[epheterson](https://clawhub.ai/user/epheterson)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to integrate Apple Music workflows, including playlist management, playback control on macOS, catalog and library search, library additions, listening history, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes destructive music-library actions such as deleting playlists, removing tracks, and changing library data.

Mitigation: Require explicit user confirmation before deleting playlists, removing tracks, changing ratings, or altering library metadata.

Risk: The skill recommends installing an unpinned third-party MCP server that would run local code.

Mitigation: Avoid the optional MCP install unless a specific trusted commit is pinned and inspected before installation.

Risk: MusicKit workflows require developer and user music tokens, which may expose account or library access if mishandled.

Mitigation: Limit token exposure, store tokens outside shared prompts and logs, and prefer direct AppleScript or official MusicKit examples for clearly user-requested actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/epheterson/skills/mcp-applemusic)
- [mcp-applemusic GitHub Repository](https://github.com/epheterson/mcp-applemusic)
- [Apple Developer MusicKit Keys](https://developer.apple.com/account/resources/authkeys/list)
- [Apple MusicKit Authorization](https://authorize.music.apple.com/woa)
- [Apple Music API](https://api.music.apple.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with AppleScript, Python, bash, JSON, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes macOS AppleScript guidance, MusicKit API request examples, and MCP server setup guidance.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence; artifact frontmatter says 0.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
