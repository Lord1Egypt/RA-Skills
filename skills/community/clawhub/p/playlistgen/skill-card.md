## Description:

Generate natural language playlists from a local music library using LLMs after indexing music files into a searchable catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asriverwang](https://clawhub.ai/user/asriverwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up a local music indexer and player, enrich their music library with LLM-generated metadata, and generate curated playlists from natural language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local HTTP server is unauthenticated and can expose the music library or consume the user's AI API account if reachable from a network.

Mitigation: Run it only on a trusted machine, bind or firewall it for localhost-only access unless authentication and network controls are added, and avoid exposing it to LAN or public networks.

Risk: Music metadata, playlist prompts, and API credentials are involved in calls to Anthropic or MiniMax.

Mitigation: Protect the .env file, use provider keys with appropriate account limits, and review provider data handling before indexing or generating playlists.

Risk: The startup script can terminate another process that is using the configured port.

Mitigation: Check port ownership before starting the service, choose a dedicated port, and avoid running the startup script with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asriverwang/skills/playlistgen)
- [README.md](artifact/README.md)
- [MUSIC_RULES.md](artifact/MUSIC_RULES.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API request examples, and JSON response shapes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local configuration, a SQLite music catalog, playlist records, logs, and generated catalog vocabulary files during setup and operation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
