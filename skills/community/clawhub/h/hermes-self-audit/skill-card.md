## Description: <br>
Audits Hermes Agent self-modification behavior, including skill changes, curator status, memory provider health, and configuration drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hermes Agent operators, SREs, and teams concerned with agent self-change use this skill to generate scheduled or on-demand audit reports on skill changes, curator activity, memory provider status, and configuration drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports may be delivered to the wrong chat target and expose local agent configuration or change history. <br>
Mitigation: Use a private delivery target and verify the chat destination before enabling a scheduled cron run. <br>
Risk: Scheduled audits can continue after they are no longer wanted, producing recurring reports and local logs. <br>
Mitigation: Remove the scheduled job or local log when automatic audit reporting is no longer needed. <br>
Risk: The skill reports anomalies but does not remediate them. <br>
Mitigation: Review reported changes and inspect Hermes state before taking corrective action. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/freepengyang/hermes-self-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown audit report with inline shell commands and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chat-platform delivery instructions and a local audit log path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
