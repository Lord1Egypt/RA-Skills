## Description: <br>
A standalone command-line skill that lets an agent query and control a Plex Media Server, including library search, playback-device discovery, and playback controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ymgenc](https://clawhub.ai/user/ymgenc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a Plex Media Server from command-line actions, including server information lookup, media search, active-client listing, playback control, and Continue Watching retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Plex token can expose library data, viewing activity, active clients, and playback control. <br>
Mitigation: Install only when that access is acceptable, provide the token through environment variables, and review playback-changing actions such as play, pause, resume, and stop before execution. <br>
Risk: The search cache stores media names, genres, and artist names in the system temporary directory. <br>
Mitigation: Delete plex_media_cache.json from the temporary directory if local media metadata is sensitive or after using the skill on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ymgenc/plex-control) <br>
- [Skill metadata](artifact/metadata.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Structured JSON from CLI actions, with Markdown instructions for setup and command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PLEX_URL and PLEX_TOKEN environment variables; uses uv, python3, and the plexapi Python dependency.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
