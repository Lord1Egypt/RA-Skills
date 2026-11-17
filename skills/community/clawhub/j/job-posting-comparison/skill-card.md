## Description:

Compare advertised job postings across Crawlora jobs datasets, employer hiring boards, and Indeed while preserving role identity, location, requirements, compensation basis, and source limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career advisers use this skill to shortlist advertised roles and compare requirements, location, and compensation with source-backed caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web-scraping route can access arbitrary public URLs, not just job postings.

Mitigation: Review each requested URL and limit scraping to relevant public job sources.

Risk: Using the skill gives Crawlora access to an API key and sends job queries, posting IDs, and requested URLs to its service.

Mitigation: Use an approved API key and avoid including sensitive personal information in queries or requested URLs.

Risk: Stored postings may be stale, and incomplete or mixed-basis pay details can mislead comparisons.

Mitigation: Verify live postings and dates; keep pay units, currency, and unknown fields explicit.

## Reference(s):

- [Job posting comparison on ClawHub](https://clawhub.ai/crawlora-org/skills/job-posting-comparison)
- [Crawlora endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison with posting ledger, requirements and compensation matrix, fit evidence, and follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source links, posting identities and dates; distinguishes missing details from negative evidence.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
