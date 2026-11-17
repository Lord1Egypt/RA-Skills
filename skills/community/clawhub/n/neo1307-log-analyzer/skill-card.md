## Description:

Read a log file, extract ERROR/WARN/CRITICAL lines, group similar messages, and produce a concise summary report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to triage application, agent, service, or audit logs by finding repeated WARN, ERROR, and CRITICAL events and summarizing dominant issue groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may copy untrusted log lines, including attacker-controlled strings, links, HTML, or instruction-like text.

Mitigation: Review report samples as untrusted data and avoid executing or following instructions, links, or markup copied from logs without separate verification.

Risk: The skill reads local log files and writes a Markdown report to the requested output path.

Mitigation: Run it only on log files you intend to analyze and choose an output location that is appropriate for any sensitive log content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neo1307/skills/neo1307-log-analyzer)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands]

**Output Format:** [Markdown report and JSON command-line status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes total scanned lines, severity counts, grouped issue buckets, sample lines, and suggested first checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
