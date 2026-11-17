## Description:

Query Google Analytics 4 (GA4) data directly via the Analytics Data API for website analytics such as top pages, traffic sources, sessions, users, conversions, bounce rate, custom date ranges, filters, and multi-metric reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operators use this skill to retrieve GA4 reporting data from properties they can access without routing analytics through a third-party proxy. It supports common web analytics workflows including top pages, traffic sources, landing pages, campaign performance, device breakdowns, country breakdowns, filters, and custom date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Google OAuth client secret and refresh token, which can grant read-only access to GA4 data if exposed.

Mitigation: Store GOOGLE_CLIENT_SECRET and GOOGLE_REFRESH_TOKEN in a protected secret store or local environment and do not commit or paste them into shared logs, chats, or issues.

Risk: Installing token-generation dependencies with an unpinned pip command may introduce dependency-chain uncertainty.

Mitigation: Prefer the bundled ga4_auth.py setup path where possible, or review and pin any external dependency before installing it.

Risk: Queries can return sensitive website analytics from any GA4 property the Google account can access.

Mitigation: Install and run the skill only for accounts and GA4 properties where read-only analytics access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeninja23/skills/native-google-analytics)
- [Publisher profile](https://clawhub.ai/user/codeninja23)
- [Google Analytics Data API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Google Analytics Data API enablement page](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)
- [Google Analytics](https://analytics.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and formatted table output from GA4 queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GA4_PROPERTY_ID, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN; query output is printed to stdout.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
