## Description: <br>
Mission Control is a macOS-native web dashboard for monitoring and controlling an OpenClaw agent with live chat, cron management, task workshop, scout engine, cost tracking, and related controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jzineldin](https://clawhub.ai/user/Jzineldin) <br>

### License/Terms of Use: <br>
BSL 1.1 (converts to MIT 2030) <br>


## Use Case: <br>
OpenClaw users and developers use Mission Control to monitor and control a local OpenClaw agent, manage conversations, scheduled jobs, delegated tasks, cost tracking, installed skills, and model settings from a browser dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing Mission Control gives a local web app access to the OpenClaw gateway token and broad agent-control features. <br>
Mitigation: Install only after reviewing and trusting the project and its dependencies, and start with a low-risk OpenClaw profile. <br>
Risk: The install flow clones an external project and installs npm dependencies without pinning a commit in the submitted instructions. <br>
Mitigation: Pin the repository to a known commit and review npm dependencies before installing or updating. <br>
Risk: A persistent service or network-exposed dashboard can expand access to agent controls. <br>
Mitigation: Keep the server bound to localhost, avoid exposing it without authentication, and inspect the systemd service before enabling persistence. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Jzineldin/openclaw-mission-control) <br>
- [Project homepage](https://github.com/Jzineldin/mission-control) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installation and configuration guidance for a local Node.js dashboard.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
