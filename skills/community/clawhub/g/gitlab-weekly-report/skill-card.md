## Description: <br>
Generates weekly reports by querying a user's GitLab commit activity for a specified date range and organizing the results by project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoutianwang](https://clawhub.ai/user/zhoutianwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to collect GitLab commit activity for a user and turn it into a weekly status report. It is intended for summarizing personal development work across GitLab projects and branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles GitLab project names, branch names, commit messages, activity history, and personal access tokens. <br>
Mitigation: Use a least-privilege expiring token, avoid sharing tokens in chat or shell history, and rotate credentials after testing. <br>
Risk: The bundled script invokes curl with TLS certificate verification disabled. <br>
Mitigation: Review or remove the TLS-bypass behavior before using the script with a real GitLab server. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhoutianwang/gitlab-weekly-report) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [gitlab_weekly_report.py](artifact/gitlab_weekly_report.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown weekly report with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitLab personal access token, user ID, date range, and configured GitLab base URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
