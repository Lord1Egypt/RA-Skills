## Description:

Validate test reports and calibration certificates against ISO/IEC 17025:2017 Clause 7.8 content requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1003429073](https://clawhub.ai/user/1003429073)

### License/Terms of Use:

MIT-0

## Use Case:

External users and quality teams use this skill to review test reports, calibration certificates, conformity statements, sampling reports, and amended reports before release. It checks required ISO/IEC 17025:2017 Clause 7.8 report content, uncertainty statements, conformity decision rules, opinion labeling, amendment handling, and unit usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can identify report content issues, but its compliance output may be incomplete or mistaken if used as the sole approval basis.

Mitigation: Treat results as a review aid and verify findings against the official ISO/IEC 17025:2017 standard and the laboratory's quality procedures before release.

Risk: The artifact references a clause text file that is not included in the package.

Mitigation: Use an authoritative copy of ISO/IEC 17025:2017 Clause 7.8 when checking clause wording or resolving borderline cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1003429073/skills/iso17025-report-guard)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist and nonconformity summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Intended as a review aid; users should verify conclusions against the official standard and laboratory quality procedures.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
