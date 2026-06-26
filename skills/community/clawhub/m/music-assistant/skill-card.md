## Description: <br>
Control Music Assistant playback, volume, queues, library search, and player status through a local Music Assistant server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodrigosiviero](https://clawhub.ai/user/rodrigosiviero) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent control a configured Music Assistant server for playback, queue management, volume changes, library search, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Music Assistant access token, which could allow unwanted control if exposed. <br>
Mitigation: Treat MA_TOKEN like a password, keep it out of logs and screenshots, and rotate it if it is exposed. <br>
Risk: Authenticated Music Assistant requests over an untrusted network could expose the token or allow unintended access. <br>
Mitigation: Use HTTPS when available or restrict use to a trusted local network. <br>
Risk: If MA_PLAYER is not set, the CLI auto-detects the first available player and may control the wrong device. <br>
Mitigation: Set MA_PLAYER explicitly when the agent should control a specific player. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rodrigosiviero/music-assistant) <br>
- [Music Assistant API documentation](http://YOUR_SERVER:8095/api-docs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MA_URL and MA_TOKEN; MA_PLAYER is optional for selecting a specific player.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
