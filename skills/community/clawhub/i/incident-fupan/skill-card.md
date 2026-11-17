## Description:

事故复盘 / Incident Fupan provides a structured root cause analysis workflow for production failures, outages, bugs, near-misses, and agent mistakes, generating incident reports with timelines, 5 Whys analysis, impact assessment, fixes, prevention actions, and defensive rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scytheshan-pixel](https://clawhub.ai/user/scytheshan-pixel)

### License/Terms of Use:


## Use Case:

Developers, operators, and incident responders use this skill to conduct evidence-based postmortems for production incidents, outages, agent errors, and near-misses. It helps produce a sourced incident report, identify actionable root causes, and convert incident patterns into prevention rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run evidence-gathering shell commands during incident review.

Mitigation: Review every command before execution and require explicit approval for commands that inspect services, logs, processes, or git state.

Risk: Incident reports may contain sensitive operational or incident details.

Mitigation: Control where reports are stored and redact sensitive details before saving or sharing incident records.

Risk: The skill can ask agents to store lessons in long-term memory or update AGENTS.md, TOOLS.md, or related skill rules.

Mitigation: Disable or require explicit approval for long-term memory writes and behavior-changing file edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scytheshan-pixel/skills/incident-fupan)
- [Postmortem Report Template](references/report-template.md)
- [Incident-to-Rule Pattern Library](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown incident report with sourced timeline, root cause analysis, action items, and optional shell commands for evidence collection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report language matches the user's language; the skill may save reports under ~/incidents/ and may propose memory or skill-rule updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
