## Description:

Guides pharmacists, MTM providers, pharmacy residents, and APPE students through a draft Comprehensive Medication Review for patients on multiple medications, including Beers/STOPP-START screening, drug-therapy problem identification, Medication Action Plan, and prescriber SBAR preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Pharmacists, MTM providers, pharmacy residents, and APPE students use this skill to structure CMR intake, reconciliation, medication-risk screening, DTP analysis, and draft patient and prescriber communications. A licensed pharmacist must verify the draft packet before any patient, prescriber, dispense, or therapy action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive patient health information during medication review.

Mitigation: Avoid entering unnecessary identifiers, keep PHI within the active clinical workflow, and use initials or minimal patient descriptors where possible.

Risk: Draft medication recommendations, interaction calls, guideline citations, or dose adjustments could be incomplete, outdated, or clinically inappropriate.

Mitigation: Require licensed-pharmacist review of every drug, dose, indication, interaction, citation, and recommendation before prescriber communication or patient action.

Risk: Patient-facing wording could be misread as authorization to change prescription therapy.

Mitigation: Keep the packet labeled draft-only and route prescription starts, stops, substitutions, and dose changes through prescriber concurrence.

## Reference(s):

- [Medication Therapy Review on ClawHub](https://clawhub.ai/archlab-space/skills/medication-therapy-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft CMR packet with structured tables and SBAR sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only clinical review artifact requiring licensed-pharmacist verification and sign-off.]

## Skill Version(s):

0.1.1 (source: server release metadata and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
