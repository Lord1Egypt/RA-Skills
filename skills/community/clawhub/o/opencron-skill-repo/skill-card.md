## Description: <br>
Visual cron job dashboard for OpenClaw with live countdown timers, run history, and calendar views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firstfloris](https://clawhub.ai/user/firstfloris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy and maintain an OpenCron dashboard for OpenClaw cron jobs, including job status, upcoming schedules, and run history. It helps agents provide dashboard access instructions after cron job runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dashboard URLs can include an access token and may expose cron metadata, prompts, outputs, or run history if shared broadly. <br>
Mitigation: Treat token-bearing OpenCron URLs as secrets, prefer localhost or an authenticated reverse proxy, and avoid posting the URL in public logs or job output. <br>
Risk: The deployment script fetches dashboard assets from unpinned remote content. <br>
Mitigation: Pin, vendor, or review the dashboard asset before production use and re-review updates before redeploying. <br>
Risk: The background sync loop copies cron job data into a served dashboard location. <br>
Mitigation: Review what cron data is exposed, limit network access, and use token validation, rate limiting, and security headers when serving externally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/firstfloris/opencron-skill-repo) <br>
- [OpenCron dashboard project](https://github.com/firstfloris/opencron) <br>
- [OpenCron skill repository](https://github.com/firstfloris/opencron-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown with inline shell commands and dashboard URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May deploy cron.html and cron-data.json under the OpenClaw canvas directory and keep cron-data.json synchronized on a 30-second loop.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
