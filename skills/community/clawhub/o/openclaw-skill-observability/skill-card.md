## Description:

Provides observability tools for OpenClaw by reporting recent errors and estimating API usage costs over the last 24 hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erain](https://clawhub.ai/user/erain)

### License/Terms of Use:

MIT

## Use Case:

Bot owners, developers, and operators use this skill to inspect OpenClaw session costs and recent failures without opening a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose raw OpenClaw gateway log lines and session details through chat, including potentially sensitive prompts, identifiers, file paths, URLs, or tokens.

Mitigation: Limit installation and use to trusted operators; redact log output, omit or truncate session identifiers and titles, and document journal access before broader deployment.

Risk: Cost reports are estimates based on recent session metadata and a hardcoded pricing table, so totals may be incomplete or stale.

Mitigation: Use the report for operational awareness and verify billing-sensitive totals against provider billing records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erain/skills/openclaw-skill-observability)
- [Publisher Profile](https://clawhub.ai/user/erain)
- [Product Requirements Document](docs/PRD_MVP.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown and plain text returned by agent tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates depend on a hardcoded pricing table and recent OpenClaw session metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
