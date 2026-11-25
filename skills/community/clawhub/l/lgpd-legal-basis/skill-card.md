## Description:

Choose and document the LGPD lawful basis for mapped personal-data processing activities, including common and sensitive data and data involving children or adolescents, and produce `.lgpd/legal-basis.md` plus legitimate-interest assessments in `.lgpd/lia/{slug}.md`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy teams use this skill after mapping processing activities, or while designing a feature, to choose and document a lawful basis under Brazil's LGPD. It provides decision guidance and Markdown templates for legal-basis records and legitimate-interest assessments.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: A selected lawful basis may be inaccurate if the processing activity, purpose, or data categories are incomplete, especially for sensitive data or minors.

Mitigation: Confirm the activity against the current data map and have qualified Brazilian privacy counsel review the basis and any required legitimate-interest or best-interest assessment.

Risk: The security review was partial because some local paths referenced by the skill were absent from the scanned bundle.

Mitigation: Check that referenced project files are present before use and review those files alongside the skill.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-legal-basis)
- [ClawHub release](https://clawhub.ai/goul4rt/skills/lgpd-legal-basis)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown guidance and templates for `.lgpd/legal-basis.md` and `.lgpd/lia/{slug}.md`]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation is organized per processing activity and should be kept in sync with `.lgpd/data-map.md`.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
