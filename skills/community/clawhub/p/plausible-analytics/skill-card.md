## Description:

Query and analyze website analytics from Plausible Analytics. Use when you need to check real-time visitors, get page views and visitor statistics for a time period, analyze traffic sources or top pages, examine geographic distribution, or generate analytics reports and insights for websites tracked with Plausible Analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:


## Use Case:

External teams, site owners, and developers use this skill to query Plausible Analytics for real-time visitor counts, aggregate traffic metrics, and breakdowns by page, source, device, browser, operating system, or country.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses PLAUSIBLE_API_KEY to query Plausible Analytics for site IDs the key can access.

Mitigation: Install only when agents are allowed to query those Plausible sites, and scope or rotate the API key according to local policy.

Risk: Returned analytics can include visitors, pageviews, sources, pages, referrers, devices, browsers, operating systems, and countries in agent output.

Mitigation: Review analytics reports before sharing them and avoid sending sensitive traffic data to untrusted channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/plausible-analytics)
- [Plausible aggregate stats API endpoint](https://plausible.io/api/v1/stats/aggregate)
- [Plausible realtime visitors API endpoint](https://plausible.io/api/v1/stats/realtime/visitors)
- [Plausible breakdown stats API endpoint](https://plausible.io/api/v1/stats/breakdown)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON analytics responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLAUSIBLE_API_KEY and an authorized Plausible site ID; scripts return current or historical analytics only for accessible sites.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
