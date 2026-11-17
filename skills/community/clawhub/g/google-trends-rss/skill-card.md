## Description:

Fetch and structure Google Trends daily trending-search data by country/region via the public RSS feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsjwong](https://clawhub.ai/user/wsjwong)

### License/Terms of Use:


## Use Case:

External users, analysts, and developers use this skill to fetch daily Google Trends by geo and export trend rows with related news context for reports, Sheets, or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Google Trends over the network.

Mitigation: Run it only where outbound access to Google Trends is expected, and account for Google-controlled availability and latency.

Risk: The skill can write user-requested JSON or CSV exports when --out is used.

Mitigation: Use trusted workspace or temporary output paths and review generated files before importing them into Sheets or reports.

Risk: Google Trends RSS feed fields and coverage can change.

Mitigation: Keep parsing defensive and verify trend rows against the current feed before relying on them in reports.

## Reference(s):

- [Google Trends Connector Notes](references/google-trends-connector-notes.md)
- [Google Trends RSS endpoint](https://trends.google.com/trending/rss)
- [Legacy Google Trends daily RSS endpoint](https://trends.google.com/trends/trendingsearches/daily/rss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal table, JSON, CSV, or Markdown trend rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports geo, limit, sort order, output format, timeout, and optional JSON/CSV file export.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
