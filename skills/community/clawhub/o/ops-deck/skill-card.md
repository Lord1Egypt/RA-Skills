## Description: <br>
Full operational dashboard for AI agent setups, including cron job calendar, agent intel feeds, security audit panel, network infrastructure map, code search, repo architecture viewer, prompt library, and sprint backlog tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, indie teams, students, and homelab operators use this skill to set up a local operations dashboard for AI agent stacks. It guides creation of local UI, API, code search, prompt library, security-status, infrastructure, journal, memory, and backlog views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local dashboard services may expose operational data if bound to untrusted interfaces. <br>
Mitigation: Keep services bound to trusted local interfaces and review the example API code before deployment. <br>
Risk: Code search or dashboard data files may index or display repository secrets or sensitive operational details. <br>
Mitigation: Review repositories and JSON data sources before indexing or loading them into the dashboard. <br>
Risk: PM2 startup configuration can make background services persist across reboots. <br>
Mitigation: Enable PM2 startup only when persistent local services are intended. <br>


## Reference(s): <br>
- [Ops Deck ClawHub page](https://clawhub.ai/solomonneas/ops-deck) <br>
- [Related Ops Deck Lite skill](https://clawhub.com/solomonneas/ops-deck-lite) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JavaScript snippets, JSON examples, and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for local services and optional data refresh scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
