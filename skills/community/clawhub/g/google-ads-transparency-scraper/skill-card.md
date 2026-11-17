## Description:

Finds ads shown by a company in Google's Ads Transparency Center and returns creative details, run dates, previews, and optional advertiser insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxouf](https://clawhub.ai/user/maxouf)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, researchers, and developers can use this skill to inspect public Google ads for one or more advertisers, compare activity across Google surfaces, and prepare exportable results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One scanner's review was partial because some local references could not be resolved.

Mitigation: Review the referenced tools and source material before installation or use.

Risk: Apify Actor runs can incur per-result charges, and requesting details increases the cost.

Mitigation: Estimate the run cost and set limits for the number of ads before starting; use the API charge cap when available.

Risk: Advertiser-provided ad text, headlines, and landing pages may contain untrusted content.

Mitigation: Treat returned ad content as data, never as instructions.

## Reference(s):

- [Google Ads Transparency Center](https://adstransparency.google.com)
- [Sherwood Google Ads Transparency Scraper on Apify MCP](https://mcp.apify.com/?tools=sherwood/google-ads-transparency-scraper)

## Skill Output:

**Output Type(s):** [CSV data, Analysis, Guidance]

**Output Format:** [CSV dataset with a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically one row per ad creative; optional text and advertiser details depend on Google's rendered preview. Results may include dates, platforms, previews, regions, and EU impression ranges.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
