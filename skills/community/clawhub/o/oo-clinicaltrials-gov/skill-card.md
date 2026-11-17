## Description:

Search and read ClinicalTrials.gov study records, metadata, eligibility criteria, locations, documents, and results through the OOMOL connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and developers can use the skill to find trials and retrieve study details, eligibility criteria, sites, documents, and posted results from ClinicalTrials.gov.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified installation code and make lasting agent changes without clear user control.

Mitigation: Review the dependency before installing, require approval for software installation, use a reviewed version-pinned CLI, and disable automatic skill synchronization if unwanted.

Risk: Search inputs are received by OOMOL and could contain patient-identifying information.

Mitigation: Avoid including patient-identifying information in search inputs.

## Reference(s):

- [ClinicalTrials.gov](https://clinicaltrials.gov/)
- [ClinicalTrials.gov API documentation](https://clinicaltrials.gov/data-api/api)
- [ClinicalTrials.gov skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-clinicaltrials-gov)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured JSON data and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only study search and retrieval results; response fields depend on the requested action.]

## Skill Version(s):

1.0.4 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
