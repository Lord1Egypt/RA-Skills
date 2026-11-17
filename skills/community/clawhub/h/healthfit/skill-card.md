## Description:

HealthFit is a personal health management skill that integrates workout planning, nutrition guidance, health data tracking, TCM constitution support, solar-term wellness, tongue self-exam workflows, and sexual-health record handling through four advisor roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

External users use HealthFit to create a personal health profile, receive fitness and nutrition guidance, track workouts and body metrics, generate progress summaries, and access TCM-oriented wellness workflows. The skill is intended for wellness support and self-tracking, not medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health and sexual-health records may be stored as plaintext in the skill workspace.

Mitigation: Use the skill only in a trusted local workspace, avoid entering sexual-health details unless needed, and confirm encryption, file permissions, retention, export, and deletion behavior before relying on it for sensitive records.

Risk: Broad natural-language triggers can load private profile context more easily than expected.

Mitigation: Use explicit HealthFit commands for intended actions and confirm before opening or updating sensitive modules.

Risk: Wellness, nutrition, exercise, and TCM responses can be mistaken for medical diagnosis or treatment.

Mitigation: Treat outputs as general wellness guidance and seek qualified medical care for symptoms, chronic conditions, medication questions, sexual-health concerns, or abnormal health signals.

## Reference(s):

- [HealthFit ClawHub Skill Page](https://clawhub.ai/chenchen913/skills/healthfit)
- [Evidence Base](references/evidence_base.md)
- [Storage Schema](references/storage_schema.md)
- [Commands](references/commands.md)
- [Sexual Health Profiling Flow](references/onboarding_sexual_health.md)
- [NSCA Position Statements](https://www.nsca.com/about-us/position-statements/)
- [ExRx.net Exercise Library](https://exrx.net/Lists/Directory)
- [National Standard Information Public Service Platform](https://std.samr.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversational responses with optional JSON, CSV, or Markdown export files and shell command suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local profile, log, draft, backup, export, and SQLite data files in the skill workspace.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and changelog report 3.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
