## Description:

Scans the Meta Ad Library API to count active ads, identify formats and ad types, track the longest-running active ad, and estimate spend for a brand when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Developers and marketing engineering teams use this skill to implement a Meta Ad Library collector for brand audit reports. It helps summarize active ad volume, creative formats, ad categories, longest-running ads, and available spend ranges from public Meta ad data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meta API access token and sends brand lookup data to Meta.

Mitigation: Provide credentials through managed environment variables or a secret store, restrict token permissions to the required API access, and use the skill only when Meta data sharing is acceptable.

Risk: The artifact defaults ad_reached_countries to the United States, which may not match non-US audit scopes.

Mitigation: Set the country filter to the audit's target geography before relying on the collected results.

Risk: The artifact notes that the first page of 100 ads may be sufficient for audits, but brands with many ads can require pagination.

Mitigation: Enable cursor pagination when complete ad coverage is required for high-volume brands.

## Reference(s):

- [Meta Ad Library API endpoint](https://graph.facebook.com/v19.0/ads_archive)
- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/meta-ads-collector)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript interfaces, API parameters, environment variable names, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Meta API credentials and returns graceful fallback data with an error field when collection fails.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
