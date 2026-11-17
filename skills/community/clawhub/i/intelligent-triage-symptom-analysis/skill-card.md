## Description:

Provides rule-based symptom extraction, red-flag detection, five-level triage classification, differential diagnosis suggestions, and recommendations for preliminary medical triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxcg](https://clawhub.ai/user/andyxcg)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare providers, telemedicine teams, and developers use this skill to turn symptom descriptions, demographics, and optional vital signs into preliminary urgency guidance. It is decision support only and requires qualified human review for clinical or emergency decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical triage output may be incomplete, incorrect, or unsupported by clinical validation.

Mitigation: Treat the skill as limited rule-based decision support and require qualified clinical review before using outputs for patient care or emergencies.

Risk: Sensitive symptom history may be stored locally by default.

Mitigation: Avoid entering real patient identifiers or detailed medical information, and use --no-save-history when possible.

Risk: The auto-evolution daemon can repeatedly execute code in the skill directory.

Mitigation: Do not run the auto-evolution daemon; review and scan any code changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxcg/skills/intelligent-triage-symptom-analysis)
- [Triage systems reference](references/triage-systems.md)
- [Disease database reference](references/disease-database.md)
- [Clinical specifications](references/clinical-specs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime output is JSON triage assessment data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include triage level, urgency, red flags, differential diagnosis suggestions, recommendations, trial or billing status, and optional saved history.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
