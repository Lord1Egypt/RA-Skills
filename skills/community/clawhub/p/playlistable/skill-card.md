## Description:

Playlistable creates AI-powered Spotify playlists, searches songs or artists, suggests playlist moods, and manages playlists through the Playlistable MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brackyt](https://clawhub.ai/user/brackyt)

### License/Terms of Use:


## Use Case:

External users and developers use Playlistable to authenticate to Spotify, generate playlists from mood prompts, search Spotify music, and list, edit, or delete playlists from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Spotify-connected bearer key locally in config/auth.json.

Mitigation: Treat config/auth.json as a secret, avoid committing or sharing it, and prefer PLAYLISTABLE_API_KEY through a managed secret store when available.

Risk: The skill exposes playlist deletion through delete_playlist.

Mitigation: Require clear user confirmation before running delete_playlist and verify the target playlist ID before execution.

Risk: Generated playlists are documented as public on Spotify.

Mitigation: Tell users that generated playlists may be public before creation, especially when prompts or track selections may reveal preferences.

## Reference(s):

- [Playlistable MCP API Reference](references/api_reference.md)
- [Playlistable MCP server](https://mcp.playlistable.io)
- [Playlistable OAuth authorization](https://mcp.playlistable.io/authorize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a Playlistable API key from PLAYLISTABLE_API_KEY or config/auth.json; playlist generation can require polling until ready.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
