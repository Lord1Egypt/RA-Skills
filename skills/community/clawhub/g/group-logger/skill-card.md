## Description: <br>
Logs LINE group messages that match job-related keywords to CSV and summarizes saved work records on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[comphone](https://clawhub.ai/user/comphone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Service teams using LINE groups can capture job updates, customer names, and statuses into CSV logs, then request Thai-language summaries for a customer, job ID, or day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently and persistently record group chat content that matches broad job-related keywords. <br>
Mitigation: Install only in groups where admins and participants have agreed to logging; prefer dedicated work channels and explicit job commands or structured job IDs. <br>
Risk: CSV logs and daily backups may expose message content, senders, group IDs, customers, and job statuses to anyone with filesystem access. <br>
Mitigation: Restrict access to group_log.csv and backups, define retention and deletion rules, and review who can read exported files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/comphone/group-logger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown summaries and CSV log rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Silent logging mode writes matching LINE group messages to CSV; summary mode responds to @mention requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
