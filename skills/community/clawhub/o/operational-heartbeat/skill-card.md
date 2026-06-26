## Description: <br>
Automated daily health check for OpenClaw instances. Verifies memory file presence, detects stale/overdue cron jobs, and surfaces system status. Intended for scheduled execution via cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guillaumemaka](https://clawhub.ai/user/guillaumemaka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a scheduled OpenClaw health check that verifies the daily memory file, reviews cron job status, and reports operational issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create a dated local memory file and inspect cron health in the configured workspace. <br>
Mitigation: Confirm the working directory and memory path before scheduled runs, and avoid pointing it at sensitive notes unless intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guillaumemaka/operational-heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown status summary with inline commands or script snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe creation or presence of a dated local memory file and cron health counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
