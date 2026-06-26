## Description: <br>
Apple Music integration via AppleScript on macOS or the MusicKit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[epheterson](https://clawhub.ai/user/epheterson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to guide Apple Music playlist management, playback control, library search, catalog search, ratings, recommendations, and MCP server setup. It emphasizes the required library-first workflow for adding catalog songs to playlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes persistent Apple Music library edits, including playlist changes and deletion. <br>
Mitigation: Require explicit confirmation before write or delete operations and verify the target playlist or track before execution. <br>
Risk: MusicKit developer tokens, user music tokens, and .p8 keys are sensitive credentials. <br>
Mitigation: Treat tokens and keys as secrets; avoid logging them, hardcoding them, or storing them in shared files. <br>
Risk: The artifact recommends installing an external MCP server from an unpinned GitHub clone. <br>
Mitigation: Review the upstream MCP server code and pin the intended version before installation. <br>


## Reference(s): <br>
- [ClawHub Apple Music skill page](https://clawhub.ai/epheterson/mcp-applemusic) <br>
- [mcp-applemusic repository](https://github.com/epheterson/mcp-applemusic) <br>
- [Apple Developer Auth Keys](https://developer.apple.com/account/resources/authkeys/list) <br>
- [Apple Music Authorization Endpoint](https://authorize.music.apple.com/woa) <br>
- [Apple Music API](https://api.music.apple.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with AppleScript, Python, Bash, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes macOS AppleScript workflows and MusicKit API examples; token-bearing values should be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata; artifact frontmatter states 0.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
