## Description:

Finds and compares public physician, hospital, pharmacy, urgent-care, and group-practice directory records through Crawlora Healthgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents researching healthcare options use this skill to build source-attributed shortlists of providers and facilities by location, specialty, and directory attributes. It does not diagnose conditions or verify care quality, insurance coverage, costs, or appointment availability.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Provider-search parameters such as location, specialty, and optional insurance filters are sent to Crawlora using an API key.

Mitigation: Use a Crawlora key only if comfortable sharing those search parameters; do not submit patient or insurance information without the user's request.

Risk: Public directory listings, ratings, and filters may not reflect current coverage, appointments, costs, or quality of care.

Mitigation: Treat results as directory evidence, not medical advice; verify coverage, availability, and costs directly with the office or insurer.

## Reference(s):

- [Healthgrades endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/health-provider-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Source-attributed Markdown shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider or facility details, source URLs, collection times, and questions to confirm with offices or insurers.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
