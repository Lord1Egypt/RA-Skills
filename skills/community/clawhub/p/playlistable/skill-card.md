## Description: <br>
Create AI-powered Spotify playlists and discover music via Playlistable MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brackyt](https://clawhub.ai/user/Brackyt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to authenticate with Playlistable, generate Spotify playlists from mood prompts, search Spotify songs or artists, get listening-based playlist suggestions, and manage existing playlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete Spotify playlists or edit playlist contents. <br>
Mitigation: Require explicit user confirmation before deletion or edits, and repeat the target playlist name or ID before running the tool. <br>
Risk: Generated playlists are documented as public on Spotify. <br>
Mitigation: Tell users before creation that generated playlists are public and avoid using private or sensitive prompts in playlist names or descriptions. <br>
Risk: The saved config/auth.json value and PLAYLISTABLE_API_KEY grant Playlistable access to Spotify playlist operations. <br>
Mitigation: Treat the API key as a credential, keep it out of logs and shared files, and rotate or remove it when access is no longer needed. <br>


## Reference(s): <br>
- [Playlistable MCP API Reference](references/api_reference.md) <br>
- [Playlistable Skill Page](https://clawhub.ai/Brackyt/playlistable) <br>
- [Playlistable MCP Server](https://mcp.playlistable.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return Spotify playlist URLs, playlist details, track lists, search results, and authentication status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
