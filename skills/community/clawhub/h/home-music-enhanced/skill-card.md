## Description: <br>
Control whole-house music scenes combining Spotify playback with Airfoil speaker routing, with presets for morning, party, chill, focus, dinner, sleep, off, and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and automation agents use this skill on macOS to start, stop, and inspect predefined home audio scenes that combine Spotify playback with Airfoil speaker routing. It is intended for local whole-house music control where the user has already configured Spotify, Airfoil, speaker names, and playlist URIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately play, pause, route, and change volume on local speakers. <br>
Mitigation: Install and run it only on machines where local music and speaker control is intended. <br>
Risk: The bundled script contains machine-specific Spotify helper paths and Airfoil speaker names. <br>
Mitigation: Update the Spotify helper path, speaker names, and playlist URIs before use. <br>
Risk: Broad voice-style triggers may start or stop music unintentionally. <br>
Mitigation: Prefer explicit commands such as home-music party or home-music off when binding this skill to an agent. <br>
Risk: The installation instructions suggest a sudo symlink for global command access. <br>
Mitigation: Create the global symlink only if the command should be available from any shell session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/home-music-enhanced) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>
- [Spotify](https://spotify.com) <br>
- [Airfoil](https://rogueamoeba.com/airfoil/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can propose or run local commands that control Spotify playback, Airfoil speaker routing, and speaker volume.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
