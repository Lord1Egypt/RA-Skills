## Description:

Drafts Medical Nutrition Therapy documentation notes in ADIME format using the Nutrition Care Process, with assessment, PES nutrition diagnosis, intervention goals, monitoring parameters, and draft flags for licensed RD/RDN review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Registered Dietitians, dietetic interns, and nutrition support team members use this skill to turn completed nutrition assessment data into a structured draft ADIME note. It is intended for clinician review before medical record entry or payer submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The draft note may be mistaken for signed clinical documentation.

Mitigation: Keep the draft label and RD/RDN attestation placeholder, and require licensed RD/RDN review before medical record entry or payer submission.

Risk: The workflow may process sensitive health information.

Mitigation: Use the minimum necessary case details, avoid direct identifiers, and use a case ID or pseudonym only.

Risk: Nutrition recommendations may be inappropriate if clinical data, lab interpretation, or facility protocols are incomplete.

Mitigation: Flag unknown data, document interpretation caveats, and have the supervising RD/RDN verify prescriptions and calculations against facility protocol.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown DRAFT ADIME note with an RD attestation placeholder and draft flags checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires licensed RD/RDN review and signature before use in medical records or billing; directs users to avoid direct patient identifiers.]

## Skill Version(s):

0.1.0 (source: server release metadata and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
