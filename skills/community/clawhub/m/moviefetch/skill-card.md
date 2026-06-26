## Description: <br>
Download, track, and remove movies across Plex, Radarr, and qBittorrent from chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seriallazer](https://clawhub.ai/user/seriallazer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home-media users and operators use MovieFetch to check Plex, request movies through Radarr, monitor qBittorrent progress, and remove titles from a chat interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat-triggered removal can delete media files by default without a clear confirmation step. <br>
Mitigation: Make file deletion explicitly opt-in and confirmed before running removal. <br>
Risk: The skill requires credentials and service access for the user's media stack. <br>
Mitigation: Use credentials limited to trusted local Plex, Radarr, qBittorrent, and related service URLs. <br>
Risk: Ambiguous movie titles can target the wrong media item. <br>
Mitigation: Confirm exact title and year before requesting or removing a movie. <br>


## Reference(s): <br>
- [MovieFetch ClawHub listing](https://clawhub.ai/seriallazer/moviefetch) <br>
- [MovieFetch README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Tool manifest](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool results and concise chat responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Plex, Radarr, qBittorrent, and API credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
