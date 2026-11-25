## Description:

Use when an AI agent hands off or takes over a project across tools or sessions, with or without a handoff package, especially when prior project memory may be stale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hermes186](https://clawhub.ai/user/hermes186)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to prepare outgoing handoffs or verify a project takeover across agents, tools, and sessions. It helps receiving agents compare available evidence, record unknowns and conflicts, and obtain confirmation before continuing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A takeover report may overstate project history or remote state when the available baseline or repository access is incomplete.

Mitigation: State the scope and evidence limits, compare only what the baseline supports, and mark unrecoverable history or inaccessible state as unknown.

Risk: An agent could continue work based on stale assumptions or unresolved conflicts before the user approves the takeover findings.

Mitigation: Present the verification results, ask for conflict decisions, and wait for explicit user confirmation before continuing development.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hermes186/skills/project-handoff-2)
- [Source repository](https://github.com/hermes186/project-handoff)
- [Imported source commit](https://github.com/hermes186/project-handoff/commit/8996a9358dad4e8e925fd4bf607a3a0af0573f50)
- [Incoming Handoff](artifact/references/incoming.md)
- [Outgoing Handoff](artifact/references/outgoing.md)
- [Handoff Record Templates](artifact/references/record-templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Files]

**Output Format:** [Markdown verification reports and handoff records; may include repository inventory and comparison results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on available project and handoff evidence; unsupported history and inaccessible state are recorded as unknown or limitations.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
