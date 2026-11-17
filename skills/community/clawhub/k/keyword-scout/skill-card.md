## Description:

Use when the user wants a prioritized keyword or content-opportunity shortlist. Supports TrustGrowth, bounded DataForSEO requests, and validated imports; direct GSC integration is deferred for launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners and site owners use Keyword Scout to generate a prioritized shortlist of 5-10 keyword or content opportunities from TrustGrowth data, approved SEO providers, or validated imports while preserving source, observation date, confidence, and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run an unbundled local validator from a dynamically found skills root.

Mitigation: Install only in a trusted Groundcrew skills environment and verify the validator path, ownership, and integrity before using validator results in conclusions.

Risk: The skill may use user-provided exports or configured SEO providers, including paid API batches.

Mitigation: Review the source, observation date, and any paid API cost disclosure before approving a batch or relying on imported evidence.

Risk: Third-party keyword volumes and SEO scores can be estimates with partial coverage.

Mitigation: Label third-party metrics as estimates, keep unknown values unknown, and avoid traffic projections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trustgrowth/skills/keyword-scout)
- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown shortlist with evidence labels and limitations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 5-10 recommendations with query, source, observed state, intent, target page or distinct angle, confidence, and limitations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
