## Description: <br>
Queries Google Analytics 4 data directly through the Analytics Data API for website analytics such as top pages, traffic sources, sessions, users, conversions, bounce rate, custom date ranges, filters, and multi-metric reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill through OpenClaw to ask for GA4 website analytics in plain English and receive direct GA4 report queries or results for a configured property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Google OAuth client secret and refresh token to read GA4 reports for the configured property. <br>
Mitigation: Use a dedicated OAuth client and a Google account with minimum needed GA4 access; keep GOOGLE_CLIENT_SECRET and GOOGLE_REFRESH_TOKEN out of source control, chats, logs, CI output, screenshots, and shared terminals. <br>
Risk: A retained refresh token can continue granting access after setup if it is copied or no longer needed. <br>
Mitigation: Revoke or rotate the refresh token when access is no longer needed, and regenerate it only for the intended GA4 property workflow. <br>


## Reference(s): <br>
- [Google Analytics Data API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1) <br>
- [Analytics Data API enablement page](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts print formatted tables or JSON to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and GA4_PROPERTY_ID, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
