## Description: <br>
Animated pixel art desktop pet that roams the screen as an always-on-top Electron overlay, avoids the cursor and active windows, walks along screen edges, climbs walls and ceilings, and responds to agent state changes via a local HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samskrta](https://clawhub.ai/user/samskrta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to run a macOS desktop companion that visually reflects agent activity through idle, working, thinking, sleeping, and talking states. It is suited for users who want a screen mascot or local visual status indicator controlled through a localhost API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow can configure the desktop pet to start automatically at login and keep itself running. <br>
Mitigation: Use manual launch unless login persistence is specifically desired, and use the uninstall script or remove the LaunchAgent to disable persistence. <br>
Risk: The desktop pet may inspect frontmost app and window metadata to avoid active windows. <br>
Mitigation: Install only if frontmost-window awareness is acceptable for the environment, and prefer disabling or reviewing that behavior before deployment in sensitive workspaces. <br>
Risk: The app exposes a local HTTP API for state changes. <br>
Mitigation: Keep the API bound to 127.0.0.1 and avoid exposing the port to other hosts. <br>


## Reference(s): <br>
- [Mu Pet ClawHub listing](https://clawhub.ai/samskrta/mu-pet) <br>
- [Publisher profile](https://clawhub.ai/user/samskrta) <br>
- [Local state API](http://127.0.0.1:18891/state) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON API examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and local control examples for a macOS Electron desktop pet; the runtime pet exposes a localhost state API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
