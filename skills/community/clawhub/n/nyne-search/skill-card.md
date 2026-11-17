## Description:

Searches for professional profiles through the Nyne Search API using natural-language queries, optional filters, contact enrichment, pagination, and AI relevance features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfanous2](https://clawhub.ai/user/michaelfanous2)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search for professionals by role, company, location, industry, or other criteria, then review returned profile, contact, work-history, education, scoring, insight, and pagination data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose personal profile, email, and phone data.

Mitigation: Use it only for authorized people-search workflows, request or display contact details only when clearly needed, and prefer redacted or minimal summaries.

Risk: Returned demographic fields such as gender and estimated age could be misused in sensitive decisions.

Mitigation: Do not rely on gender or estimated age for sensitive, regulated, or eligibility-related decisions.

Risk: Examples write enriched search results to fixed temporary paths and show partial credential values.

Mitigation: Use private mktemp files, delete result files after use, and verify credentials without printing any portion of a secret.

## Reference(s):

- [Nyne API](https://api.nyne.ai)
- [Nyne Person Search API](https://api.nyne.ai/person/search)
- [ClawHub Skill Page](https://clawhub.ai/michaelfanous2/skills/nyne-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls that return JSON profile, contact, work-history, education, scoring, insight, and pagination data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
