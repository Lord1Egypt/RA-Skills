## Description: <br>
MusicPlaylistGen helps agents index a local music library, enrich tracks with LLM-generated metadata, and generate natural-language playlists through a local web and API server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asriverwang](https://clawhub.ai/user/asriverwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and local music-library users use this skill to configure PlaylistGen, index audio files, enrich catalog metadata with an LLM, start the local server, and generate playable playlists from natural language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music filenames, tags, catalog summaries, and playlist prompts may be sent to external AI providers during indexing and playlist generation. <br>
Mitigation: Use the skill only when that disclosure is acceptable, review the configured provider, and avoid indexing libraries whose metadata should remain private. <br>
Risk: The local server can expose the music library and generated player URLs over the network if bound or routed beyond localhost. <br>
Mitigation: Keep the service on localhost or a trusted network by default, and add firewall controls or authentication before remote or LAN exposure. <br>
Risk: The .env file stores API keys and local path configuration. <br>
Mitigation: Protect .env as a secret-bearing file, avoid sharing it, and keep it out of published artifacts and source control. <br>
Risk: The startup script kills any process already using the configured port. <br>
Mitigation: Review the selected PORT and active listeners before running start.sh, especially on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asriverwang/playlistgen) <br>
- [Publisher profile](https://clawhub.ai/user/asriverwang) <br>
- [README](artifact/README.md) <br>
- [Music rules](artifact/MUSIC_RULES.md) <br>
- [Environment sample](artifact/env.sample.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON API examples, configuration values, and generated playlist URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide local setup and can trigger local indexing, server startup, and API calls when the agent follows its workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
