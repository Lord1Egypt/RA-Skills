## Description:

Collects Instagram profile statistics, engagement metrics, posting frequency, average reactions, and top hashtags for a given handle using Apify's Instagram Profile Scraper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Developers and marketing-audit teams use this skill to add Instagram profile collection to an audit pipeline. It returns normalized metrics and graceful error data so downstream report generation can continue when collection fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram handles and public profile or post data are sent to Apify for scraping.

Mitigation: Use the skill only when that data transfer is acceptable for the organization and confirm Apify terms, token scope, expected costs, and privacy or scraping compliance requirements before production use.

Risk: Instagram data returned by Apify may be stale, cached, unavailable, or incomplete for private, missing, large, or rate-limited profiles.

Mitigation: Treat collected metrics as audit inputs rather than authoritative records, keep graceful error handling enabled, and allow downstream pipeline steps to continue when collection fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/instagram-collector)
- [Apify Instagram Profile Scraper API endpoint](https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript examples and structured data schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for returning InstagramData with follower, post, engagement, posting-frequency, reaction, hashtag, and optional error fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
