## Description:

Professional medical record drafting assistant that guides users through a three-step process to generate standardized admission records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gshatw](https://clawhub.ai/user/gshatw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and healthcare documentation workflows can use this skill to collect patient details, confirm the collected information, and draft a structured admission record. Generated content requires appropriate clinical review before use in care or official records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated records may include normal or clinical default values for information the user did not provide.

Mitigation: Require authorized clinician review before treating generated record content as clinical fact or using it in official care documentation.

Risk: Real patient information may be saved to local Markdown files without documented storage safeguards.

Mitigation: Avoid unnecessary identifiers and confirm storage location, access controls, retention, and filename handling before saving records.

## Reference(s):

- [Usage example](references/example.md)
- [ClawHub skill page](https://clawhub.ai/gshatw/skills/medical-record-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown admission record with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated records as local Markdown files when the script save helper is used.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
