## Description: <br>
Integrates with the PingCode research and development management API to query work items, test libraries, project progress, organization data, wiki content, DevOps data, weekly reports, and dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geji](https://clawhub.ai/user/geji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Development teams and project managers use this skill to let an agent retrieve PingCode project, work item, test, wiki, user, and DevOps information, update work-item fields, and produce status summaries or weekly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive PingCode company data across projects, users, wiki content, test records, DevOps records, and work history. <br>
Mitigation: Install it only with a dedicated least-privilege PingCode app, preferably read-only, and avoid broad queries in terminals or transcripts that may be logged. <br>
Risk: The skill includes commands that can update work-item fields such as assignee, dates, priority, and status. <br>
Mitigation: Grant write scopes only when they are needed and require explicit human confirmation before running update commands. <br>
Risk: Generated reports may contain sensitive project information if written to shared or synced paths. <br>
Mitigation: Write reports to controlled private locations and review them before sharing. <br>
Risk: Security evidence says most included Python files currently contain syntax errors. <br>
Mitigation: Verify and fix the scripts before relying on operational output. <br>


## Reference(s): <br>
- [PingCode Open API Documentation](references/api_docs.md) <br>
- [PingCode Open API](https://open.pingcode.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with optional JSON output from scripts and Markdown weekly report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PINGCODE_CLIENT_ID and PINGCODE_CLIENT_SECRET; scripts may call PingCode APIs and may write report files to a user-provided path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
