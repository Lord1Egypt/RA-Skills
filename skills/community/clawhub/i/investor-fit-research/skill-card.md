## Description:

Build investor and fund shortlists from Crawlora public PitchBook profiles and stored investor, fund, and company records, preserving gaps in public coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Fundraising teams and founders use this skill to research and qualify potential investors and funds for a specified company and round, with source-attributed fit and explicit unknowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and a Crawlora API key are sent to Crawlora, and requests may consume credits.

Mitigation: Use a service-scoped key, set a request and credit budget, and review queries before sending them.

Risk: Public profile previews may be incomplete or outdated; an apparent match does not establish current investment appetite.

Mitigation: Attribute sources and dates, preserve unknown criteria, and verify material claims before fundraising or investment decisions.

Risk: A research shortlist could be mistaken for permission to contact investors or share company information.

Mitigation: Require separate authorization before outreach, disclosure, or paid-data registration.

## Reference(s):

- [Investor fit research endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/investor-fit-research)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Source-attributed Markdown shortlist and criterion matrix]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence dates, unresolved questions, and conditional or rejected candidates.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
