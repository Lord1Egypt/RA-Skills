## Description:

Query Plausible Analytics API for traffic stats, referrers, conversions, and custom events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, operators, and site owners use this skill to retrieve Plausible Analytics traffic, referrer, conversion, page, device, geography, and custom event data through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a Plausible API token to a custom stored endpoint.

Mitigation: Use the default plausible.io endpoint unless intentionally using a trusted self-hosted Plausible instance, and verify any custom base URL before queries run.

Risk: Site domains and analytics query parameters are sent to the configured Plausible host.

Mitigation: Install and use the skill only when the configured Plausible host is trusted for the site's analytics data.

Risk: Local site configuration is stored under ~/plausible/.

Mitigation: Keep local Plausible memory files limited to non-secret site configuration and continue providing the API key through PLAUSIBLE_API_KEY.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/plausible)
- [Plausible skill homepage](https://clawic.com/skills/plausible)
- [Plausible realtime visitors endpoint](https://plausible.io/api/v1/stats/realtime/visitors)
- [Plausible aggregate stats endpoint](https://plausible.io/api/v1/stats/aggregate)
- [Plausible timeseries stats endpoint](https://plausible.io/api/v1/stats/timeseries)
- [Plausible breakdown stats endpoint](https://plausible.io/api/v1/stats/breakdown)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration guidance]

**Output Format:** [Markdown summaries with Plausible API query details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLAUSIBLE_API_KEY and a configured Plausible site ID.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
