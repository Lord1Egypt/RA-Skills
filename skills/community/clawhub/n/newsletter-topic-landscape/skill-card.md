## Description:

Compare editorial topics and coverage across Substack newsletters using Crawlora publication discovery and bounded public-post samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Editors, researchers, and analysts compare sampled Substack publication coverage, identify observed topic gaps, and assemble a topic-focused reading shortlist without treating samples as audience measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newsletter queries and the user-provided API key are sent to Crawlora.

Mitigation: Confirm the service is appropriate before use and protect the API key.

Risk: Public-post samples and previews may give an incomplete picture of coverage or audience.

Mitigation: Use narrow topic and date scopes, show sample sizes and missing bodies, and avoid claims about readership or market demand.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/newsletter-topic-landscape)
- [Crawlora endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown report with a publication-by-topic matrix and sampled-post evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs and dates, topic-coding basis, a reading shortlist, and sampling limitations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
