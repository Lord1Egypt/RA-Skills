## Description:

Integrates with a News Agent backend API to query articles, trigger collection and analysis tasks, retrieve dashboard data, and inspect trend and word-cloud data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swipth](https://clawhub.ai/user/swipth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect news records, monitor news analytics dashboards, analyze keyword and category trends, and trigger backend crawl, analysis, or trend jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable development bearer token can be sent to an unintended or untrusted API host.

Mitigation: Use the skill only with a trusted local or test backend, validate NEWS_API_BASE_URL before use, prefer HTTPS or loopback-only development services, and replace the fixed token with scoped user-provided authentication.

Risk: Crawl, analyze, and trend commands trigger backend jobs that may change state or consume resources.

Mitigation: Treat task triggers as privileged operations and require explicit confirmation before POST requests are run.

## Reference(s):

- [News Agent API Reference](artifact/references/api_docs.md)
- [ClawHub skill page](https://clawhub.ai/swipth/skills/news-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown usage guidance, shell commands, and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEWS_API_BASE_URL and a reachable trusted News Agent backend API.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
