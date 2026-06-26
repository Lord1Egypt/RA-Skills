## Description: <br>
Performs Jira Cloud daily work through REST API v3 and Jira Software Agile API calls, including issue search, creation, updates, comments, worklogs, boards, sprints, and transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheCyberCore](https://clawhub.ai/user/TheCyberCore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to turn Jira Cloud requests into concrete CLI HTTP calls, then parse and summarize the JSON results. It supports day-to-day Jira workflows such as triage, issue creation, comments, worklogs, assignments, transitions, boards, and sprints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real Jira Cloud actions that persist in Jira. <br>
Mitigation: Install it only when real Jira automation is intended, use a least-privilege Jira account or token, and limit project access where possible. <br>
Risk: Non-read-only operations can change issues, comments, worklogs, sprints, transitions, and issue entity properties. <br>
Mitigation: Review write requests before execution and require clear user intent for destructive or state-changing actions. <br>
Risk: Jira credentials could be exposed if tokens are echoed, logged, or embedded in commands. <br>
Mitigation: Keep credentials in environment variables, avoid printing token values, and avoid storing tokens in repository files. <br>


## Reference(s): <br>
- [Skill Source](artifact/SKILL.md) <br>
- [CLI REST Quick Reference](artifact/refs/cli-rest-quickref.md) <br>
- [Jira JSON Quick Reference](artifact/refs/jira-json-quickref.md) <br>
- [JQL Cheat Sheet](artifact/refs/jql-cheatsheet.md) <br>
- [App Embedding Quick Reference](artifact/refs/app-embedding-quickref.md) <br>
- [openClaw Environment Example](artifact/refs/openclaw_env_example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI command snippets, JSON payloads, and concise result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Jira Cloud environment variables and a scoped Jira token or bearer credential.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
