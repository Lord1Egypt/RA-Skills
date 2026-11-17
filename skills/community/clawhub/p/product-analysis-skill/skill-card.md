## Description:

Analyzes market trends and competitor products to provide data-driven recommendations for product selection and optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to analyze individual products or product batches, compare market and competitor signals, and generate product selection and optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security scan marks the release as suspicious because the included batch script can load code from outside the skill folder.

Mitigation: Review the batch analyzer before installation and run it only when the install directory is trusted and not writable by untrusted users.

Risk: Batch analysis depends on SubAgent resolution that the security guidance says should be fixed before use.

Mitigation: Avoid running the batch analyzer until the SubAgent dependency path is reviewed or corrected; use the lower-impact single-product analyzer when appropriate.

Risk: The artifact analyzer uses static pattern data and mock analysis rather than live market data.

Mitigation: Treat recommendations as preliminary guidance and validate product decisions against current market data before relying on them commercially.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/534422530/skills/product-analysis-skill)
- [Artifact README](artifact/README.md)
- [Artifact Manifest](artifact/claw.json)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [JSON analysis results, timestamped JSON batch reports, and plain-text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-product analysis can print JSON to stdout; batch analysis can write timestamped JSON report files.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
