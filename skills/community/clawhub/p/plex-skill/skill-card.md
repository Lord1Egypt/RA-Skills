## Description: <br>
Control Plex Media Server - browse libraries, search, play media, manage playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MephistoJB](https://clawhub.ai/user/MephistoJB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a Plex Media Server use this skill to browse libraries, search media, inspect sessions, and run Plex API curl commands after configuring PLEX_SERVER and PLEX_TOKEN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Plex token can grant access to the configured Plex server and expose library or session information. <br>
Mitigation: Keep the token private, prefer the least access practical, and avoid sharing generated commands that include the token. <br>
Risk: Playback or control actions could affect Plex clients or sessions unexpectedly. <br>
Mitigation: Review commands before execution and require explicit confirmation before starting playback or changing device state. <br>


## Reference(s): <br>
- [Plex](https://plex.tv) <br>
- [ClawHub Plex skill page](https://clawhub.ai/MephistoJB/plex-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided PLEX_SERVER and PLEX_TOKEN values to form Plex API requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
