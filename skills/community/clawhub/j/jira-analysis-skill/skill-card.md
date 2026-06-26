## Description: <br>
Pulls Bug data from Jira Server/Data Center, analyzes trends, priority, severity, components, resolution time, workload, aging, and labels, then helps generate an interactive self-contained HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cntesters](https://clawhub.ai/user/cntesters) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and engineering managers use this skill to collect Jira Bug data, review defect trends and workload indicators, and produce an interactive HTML report for project quality analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Jira credentials and can read internal project issue data. <br>
Mitigation: Use a least-privilege Personal Access Token scoped to the required project and avoid passing secrets directly in reusable shell history. <br>
Risk: Disabling TLS verification can expose credentials and Jira data in transit. <br>
Mitigation: Keep TLS verification enabled and use --no-verify only for controlled internal troubleshooting when the connection path is trusted. <br>
Risk: Generated HTML and Excel reports can contain confidential issue summaries, assignees, reporters, labels, and timing data. <br>
Mitigation: Store and share generated reports only in approved confidential locations with access limited to the intended project audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cntesters/jira-analysis-skill) <br>
- [Publisher profile](https://clawhub.ai/user/cntesters) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Analysis, HTML, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, structured JSON from the Jira fetch script, and a self-contained HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Jira credentials and project access; generated reports can contain confidential issue data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
