## Description:

Unified bug investigation and closure by combining source code, database, server logs, and software platform query capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate bugs with an evidence chain across logs, databases, source code, and platform queries before making root-cause conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to use database, server-log, source-code, and platform access for bug investigations without enough task-specific scoping or approval.

Mitigation: Use narrowly scoped read-only credentials, require explicit approval before production queries or log pulls, and constrain searches by service, time window, and identifiers.

Risk: Bug investigation outputs may expose sensitive operational data from logs, databases, or business systems.

Mitigation: Redact sensitive output and review the skill before installing it in environments with production data.

Risk: The skill recommends adding an external log-analysis skill when log capability is missing.

Mitigation: Independently inspect or pin the external log-analysis skill before adding it.

## Reference(s):

- [server-log-analysis](https://clawhub.ai/hgvgfgvh/server-log-analysis)
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/multi-capability-bug-closure-en)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with evidence summaries, root-cause assessment, recommendations, and verification criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include query or log-inspection commands when needed for evidence gathering.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
