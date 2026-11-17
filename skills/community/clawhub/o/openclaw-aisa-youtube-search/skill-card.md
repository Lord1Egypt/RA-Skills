## Description:

YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content researchers, and marketing teams use this skill to query YouTube search results for content planning, competitor tracking, trend discovery, keyword research, and regional audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube research queries, locale or filter parameters, and the AISA_API_KEY to AIsa's API.

Mitigation: Avoid sensitive internal project names, regulated data, and secrets in search queries; use a scoped API key where available.

Risk: Results depend on a third-party YouTube search API and may reflect ranking changes or API availability.

Mitigation: Review returned results before using them for business decisions and handle API errors or stale data in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-youtube-search)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API reference](https://docs.aisa.one/reference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to the AIsa YouTube search API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
