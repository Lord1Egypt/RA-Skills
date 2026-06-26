## Description: <br>
Launch and manage the OpenClaw Dashboard web UI for monitoring bots, agents, models, and sessions across macOS, Windows, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmanrui](https://clawhub.ai/user/xmanrui) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to start, update, and access a local dashboard for monitoring bots, agents, models, sessions, and gateway health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run code from a remote dashboard repository and its npm dependencies. <br>
Mitigation: Use it only when the publisher and remote repository are trusted, and review the dashboard source and dependency changes before invocation in sensitive environments. <br>
Risk: The skill can stop services on port 3000 and replace an existing local OpenClaw-bot-review directory when updating without git. <br>
Mitigation: Check what is using port 3000 and back up local OpenClaw-bot-review edits before running the launcher. <br>
Risk: The dashboard can expose local OpenClaw status data through a LAN URL. <br>
Mitigation: Share the LAN URL only on trusted networks and stop the background server when monitoring is complete. <br>


## Reference(s): <br>
- [ClawHub OpenClaw Bot Dashboard release](https://clawhub.ai/xmanrui/openclaw-bot-dashboard) <br>
- [OpenClaw Dashboard project](https://github.com/xmanrui/OpenClaw-bot-review) <br>
- [OpenClaw framework](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown status messages with shell commands and local or LAN access URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns localhost and LAN dashboard URLs when available, plus concise error guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
