## Description:

Compare US housing markets through Crawlora's historical housing dataset and Redfin tools, with qualified interpretation of prices, inventory, sales activity, time on market, and affordability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts compare US city, metro, county, or ZIP-code housing markets over matched periods and property types, with caveats for missing data and modeled affordability.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Housing-market search locations and filters are sent to Crawlora.

Mitigation: Use only locations and filters you are comfortable sharing; omit sensitive personal financial details unless necessary.

Risk: Exposing the Crawlora API key in chats or reports could compromise access.

Mitigation: Keep the key in the environment and do not paste it into chats or reports.

Risk: Unmatched reporting periods or modeled affordability may mislead comparisons.

Mitigation: Match measurement windows, disclose affordability assumptions and income vintage, and distinguish market aggregates from individual decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/housing-market-research)
- [Housing market endpoint reference](reference/endpoints.md)
- [Redfin Data Center and methodology](https://www.redfin.com/news/data-center/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Comparison tables with explanatory text and optional time-series charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Include measurement windows, sources, sample counts, missing-data notes, and affordability assumptions.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
