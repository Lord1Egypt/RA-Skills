## Description:

Scout helps agents conduct lawful, provenance-backed OSINT research on people, companies, and organizations, including entity resolution, cited background briefs, and source-tiered research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Scout to conduct lawful OSINT research, due diligence, and background research on people, companies, and organizations. It is intended for workflows that need cited findings, identity-resolution notes, source logs, and explicit escalation controls for paid or rate-limited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended OSINT runs and self-updates may occur if the bundled background tasks are enabled without review.

Mitigation: Review and disable cron/background tasks unless unattended runs and updates are explicitly intended.

Risk: The skill can collect and store sensitive personal data during person or organization research.

Mitigation: Run with restricted network egress, avoid broad tokens in profile environment files, and treat outputs as sensitive data subject to legal and policy limits.

Risk: OSINT results can be incomplete, stale, or incorrectly correlated across public sources.

Mitigation: Require source-backed provenance, confidence labels, and identity-resolution notes before acting on findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-scout)
- [Scout Source Waterfall](references/scout_source_waterfall.md)
- [Scout Public Records](references/scout_public_records.md)
- [Scout Schemas](references/scout_schemas.md)
- [Scout Brief Template](references/scout_brief_template.md)
- [Source Reliability](references/source_reliability.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefs with cited source logs, JSONL journal entries, Signal payloads, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include provenance, confidence, and uncertainty notes; sensitive personal data can be minimized when requested.]

## Skill Version(s):

2.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
