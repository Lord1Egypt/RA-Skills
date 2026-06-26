## Description: <br>
PLEX-CTL helps an agent search, browse, play, and control Plex Media Server libraries and clients through the Plex API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akivasolutions](https://clawhub.ai/user/akivasolutions) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to control a configured Plex environment: search media libraries, start playback, pause or resume clients, inspect currently playing sessions, browse recently added or on-deck content, and retrieve title metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Plex token locally, and that token can grant access to the user's Plex server and library metadata. <br>
Mitigation: Treat the Plex token like a password, keep it out of logs and commits, and restrict access to ~/.plexctl/config.json. <br>
Risk: Client discovery can fall back to MyPlex cloud resources when local discovery does not find a client. <br>
Mitigation: Review the cloud discovery fallback before use if the deployment requires strictly local-only behavior. <br>
Risk: Playback commands can control any reachable Plex client selected during setup or with a command option. <br>
Mitigation: Confirm the intended default client during setup and specify a client explicitly when controlling shared devices. <br>


## Reference(s): <br>
- [ClawHub PLEX-CTL release](https://clawhub.ai/akivasolutions/plex-ctl) <br>
- [Plex Web](https://app.plex.tv) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline CLI commands and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Plex server URL, Plex token, and reachable Plex client; stores configuration locally in ~/.plexctl/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
