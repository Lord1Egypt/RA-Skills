## Description:

Run a code-level privacy discovery, gap analysis, and prioritized retrofit plan for an existing software project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goul4rt](https://clawhub.ai/user/goul4rt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy teams use this skill to inspect an existing software project for privacy-related implementation gaps and produce an evidence-based, prioritized retrofit plan. It separates code observations from issues that need legal or organizational validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, and nine referenced local paths could not be reviewed, leaving some uncertainty about the skill contents.

Mitigation: Review the referenced source files and scan the complete skill before installation or use.

Risk: A code-level gap analysis may not establish legal or organizational compliance on its own.

Mitigation: Have findings that depend on legal or organizational decisions reviewed by the responsible specialists before treating them as compliance conclusions.

## Reference(s):

- [Source repository: lgpd-legacy-retrofit](https://github.com/goul4rt/lgpd-skills/tree/main/skills/lgpd-legacy-retrofit)
- [ClawHub skill release](https://clawhub.ai/goul4rt/skills/lgpd-legacy-retrofit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown discovery report and prioritized gap analysis saved as .lgpd/discovery.md and .lgpd/gaps.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates engineering actions from external legal and organizational validation; pauses for confirmation before proceeding to L2.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
