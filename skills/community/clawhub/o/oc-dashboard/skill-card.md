## Description: <br>
A real-time monitoring dashboard for OpenClaw agents that tracks agents, sub-agents, cron jobs, costs, project progress, activity, memory, logs, and session replay in a dark-mode UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrpixelraf](https://clawhub.ai/user/mrpixelraf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to monitor local OpenClaw agent activity, project state, costs, cron jobs, memory files, logs, and session history from a browser dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can expose private local OpenClaw sessions, memory files, costs, project data, and logs through its server. <br>
Mitigation: Run it only on a trusted machine and trusted network, avoid exposing port 3721 beyond localhost unless access controls are added, and stop the server when monitoring is complete. <br>
Risk: LAN access can make sensitive dashboard data reachable from other devices on the same network. <br>
Mitigation: Use LAN access only on trusted networks and restrict network exposure when private OpenClaw data is present. <br>


## Reference(s): <br>
- [OpenClaw Dashboard on ClawHub](https://clawhub.ai/mrpixelraf/oc-dashboard) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw Dashboard demo](https://openclaw-dashboard-demo.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for running a local React, Vite, Tailwind CSS, Express, and Chart.js monitoring dashboard.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
