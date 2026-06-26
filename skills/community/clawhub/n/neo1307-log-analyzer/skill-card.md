## Description: <br>
Reads a log file, groups WARN, ERROR, and CRITICAL lines, and produces a summary report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to triage application, agent, service, or audit logs by isolating important severity lines and grouping repeated warning or failure patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may copy log lines that contain secrets, personal data, or sensitive operational details. <br>
Mitigation: Review logs before analysis and scrub the generated Markdown report before sharing it. <br>
Risk: The grouped findings are a triage artifact and may not identify the full root cause of an incident. <br>
Mitigation: Validate grouped messages against the original logs and operational context before taking remediation action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neo1307/neo1307-log-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with JSON execution status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected local log file and reports total scanned lines, severity counts, grouped issue buckets, sample lines, and suggested first checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
