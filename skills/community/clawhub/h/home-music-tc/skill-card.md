## Description: <br>
Control whole-house music scenes combining Spotify playback with Airfoil speaker routing, with quick presets for morning, party, chill, and focus modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home users and developers use this skill on macOS to start, stop, inspect, and customize whole-house music scenes that combine Spotify playback with Airfoil speaker routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control local Spotify playback and Airfoil speaker routing, so broad voice or terminal triggers could change household audio unexpectedly. <br>
Mitigation: Install only on a Mac where this control is intentional, prefer explicit commands such as home-music party or home-music stop, and review the configured scenes before use. <br>
Risk: The optional sudo symlink makes the command available system-wide. <br>
Mitigation: Skip the symlink unless global access is needed, or inspect the script first and keep execution scoped to the skill directory. <br>
Risk: Default playlist IDs, speaker names, and the Spotify helper path are environment-specific. <br>
Mitigation: Update playlist URIs, speaker names, and helper paths to match the target Mac before relying on scenes. <br>


## Reference(s): <br>
- [Home Music on ClawHub](https://clawhub.ai/terrycarter1985/home-music-tc) <br>
- [Spotify](https://spotify.com) <br>
- [Airfoil](https://rogueamoeba.com/airfoil/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with bash commands and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Spotify Desktop, Airfoil, and configured local speaker and playlist names.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
