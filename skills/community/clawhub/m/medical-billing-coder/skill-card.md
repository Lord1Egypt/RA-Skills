## Description:

Use this skill when a clinician, biller, or practice manager needs to look up ICD-10 diagnosis codes, CPT procedure codes, or E&M visit level codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[optimusprime19](https://clawhub.ai/user/optimusprime19)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, billers, and practice managers use this skill to suggest ICD-10 diagnosis codes, CPT procedure codes, E&M visit levels, claim validation checks, denial risks, and draft superbills from de-identified clinical descriptions. The output is advisory and must be reviewed by a qualified medical coder or clinician before billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect code suggestions could lead to billing errors, denied claims, audit exposure, or fraud concerns.

Mitigation: Treat outputs as advisory and require review and approval by a qualified medical coder or clinician before claim submission.

Risk: Users could expose protected health information by entering names, MRNs, DOBs, addresses, or other patient identifiers.

Mitigation: Use only de-identified clinical descriptions and avoid patient-identifiable information in prompts.

Risk: CMS validation may create network egress when CMS_API_KEY is configured.

Mitigation: Confirm organizational approval before enabling CMS validation and send only billing code pairs, not clinical text.

Risk: CPT is a proprietary AMA code set and may require a license for production claim submission.

Mitigation: Confirm appropriate CPT licensing and use the skill's CPT references as advisory support rather than a substitute for licensed production resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/optimusprime19/skills/medical-billing-coder)
- [Publisher profile](https://clawhub.ai/user/optimusprime19)
- [Project homepage](https://github.com/optimusprime19/medical-billing-coder)
- [CMS Medicare Coverage Database API](https://api.cms.gov/medicare-coverage-database/v2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with code suggestions, confidence notes, validation findings, and superbill-style summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use CMS_API_KEY for CMS validation; only billing code pairs should be sent to CMS APIs, not clinical text.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
