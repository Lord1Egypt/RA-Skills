## Description:

Provides decision-support guidance for medical-device import and export pathways, with structured JSON results that require human verification against official regulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0 (listing); code MIT, documentation and theory rights reserved (artifact)

## Use Case:

Developers and compliance teams use this skill to identify possible medical-device import or export routes and required documents before checking current official requirements. It is decision support, not a regulatory determination or authorization to file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested pathways may be incomplete or inconsistent with current medical-device regulations.

Mitigation: Use only as decision support and verify each decision against current official regulatory sources before acting.

Risk: Broad tool access and proposed automatic filings or full call logs could cause unauthorized actions or expose sensitive compliance data.

Mitigation: Require explicit approval before filing, writing records, fetching external sources, or retaining logs; define redaction and secure storage rules for sensitive data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [JSON decision-support result with route, required documents, warnings, and status code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human review required; the tool does not classify devices or provide definitive destination-country requirements.]

## Skill Version(s):

1.0.2 (source: ClawHub release; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
