## Description: <br>
Visual cron job dashboard for OpenClaw - live countdown timers, run history, calendar view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firstfloris](https://clawhub.ai/user/firstfloris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to deploy a local dashboard that reads cron job definitions and run history, then serves live countdown, history, and calendar views for OpenClaw cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard exposes local cron data through an unauthenticated network service. <br>
Mitigation: Bind the server to localhost and put any wider access behind authentication or a protected reverse proxy. <br>
Risk: The dashboard relies on mutable GitHub-hosted dashboard HTML. <br>
Mitigation: Vendor or pin the dashboard HTML and review updates before enabling continuous refresh. <br>
Risk: Background nohup or watch behavior can keep the service exposed longer than intended. <br>
Mitigation: Disable automatic background startup unless continuous dashboard exposure is intentional. <br>


## Reference(s): <br>
- [ClawHub Opencron Skill Page](https://clawhub.ai/firstfloris/opencron) <br>
- [OpenCron Dashboard Repository](https://github.com/firstfloris/opencron) <br>
- [OpenCron Skill Repository](https://github.com/firstfloris/opencron-skill) <br>
- [OpenCron Dashboard Template](https://raw.githubusercontent.com/firstfloris/opencron/master/cron-dashboard.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a localhost HTTP server and generate dashboard HTML from local OpenClaw cron data.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
