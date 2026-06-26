## Description: <br>
Track skill usage across agent sessions by logging invocations to a local JSONL file and generating daily usage summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor which skills are invoked, summarize daily usage, identify unused skills, and reset or archive local analytics logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can log raw skill triggers and context across sessions, which may capture sensitive or unnecessary usage details. <br>
Mitigation: Enable it only when workspace-wide skill monitoring is intended; redact trigger text, limit which skills are logged, restrict access to logs and reports, and define retention and deletion rules. <br>
Risk: The optional scheduled report can repeatedly process and expose local analytics data. <br>
Mitigation: Review the report script, destination, and access controls before enabling the cron job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/heleni-skill-analytics) <br>
- [Publisher profile](https://clawhub.ai/user/netanel-abergel) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown reports, JSONL log entries, and shell or cron snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local analytics artifacts that may include raw trigger text, skill names, timestamps, and context labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
