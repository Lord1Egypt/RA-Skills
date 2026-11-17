## Description:

Group Logger logs LINE group messages that match work-related keywords to CSV and summarizes logged jobs or customer activity when mentioned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comphone](https://clawhub.ai/user/comphone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams managing LINE work groups use this skill to capture keyword-matched job or customer messages in a CSV log and request Thai summaries for jobs, customers, pending work, or daily activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently stores raw LINE group-chat messages that match work-related keywords.

Mitigation: Install only where group members have been informed that keyword-matching messages are logged.

Risk: CSV logs and backups may contain group-chat history, job details, customer names, and sender information.

Mitigation: Protect the CSV and backup files, define retention and deletion rules, and limit access to authorized users.

Risk: Summaries could expose information outside the intended group, customer, or job scope.

Mitigation: Restrict summary requests to authorized users and verify that responses stay within the appropriate group or customer scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/comphone/skills/group-logger)
- [Publisher profile](https://clawhub.ai/user/comphone)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [CSV log entries and Thai Markdown/text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a keyword-filtered group_log.csv file, maintains a backup CSV file, and separates records by group_id.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
